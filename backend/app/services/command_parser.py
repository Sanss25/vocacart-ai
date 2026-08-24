"""
VocaCart AI Natural Language Understanding (NLU) Engine
Robust hybrid pipeline supporting English, Hindi (Devanagari), and Hinglish (Romanized Hindi).
Extracts intent, entities (products, quantities, units, brands, categories, price limits, attributes),
and outputs full pipeline inspection telemetry.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from app.services.category_classifier import classify_category

# Multilingual number dictionary
NUMBER_WORDS = {
    # English
    "a": 1.0, "an": 1.0, "one": 1.0, "two": 2.0, "three": 3.0, "four": 4.0, "five": 5.0,
    "six": 6.0, "seven": 7.0, "eight": 8.0, "nine": 9.0, "ten": 10.0, "eleven": 11.0,
    "twelve": 12.0, "half": 0.5, "quarter": 0.25,
    # Hinglish
    "ek": 1.0, "do": 2.0, "teen": 3.0, "char": 4.0, "chaar": 4.0, "paanch": 5.0, "panch": 5.0,
    "chhah": 6.0, "che": 6.0, "saat": 7.0, "aath": 8.0, "nau": 9.0, "das": 10.0,
    "aadha": 0.5, "adha": 0.5, "dedh": 1.5, "dhai": 2.5,
    # Devanagari Hindi
    "एक": 1.0, "दो": 2.0, "तीन": 3.0, "चार": 4.0, "पांच": 5.0, "पाँच": 5.0,
    "छह": 6.0, "सात": 7.0, "आठ": 8.0, "नौ": 9.0, "दस": 10.0, "आधा": 0.5
}

# Unit dictionary
UNIT_MAP = {
    # Packets
    "packet": "packet", "packets": "packet", "pack": "packet", "packs": "packet", "pouch": "packet", "pouches": "packet",
    "पैकेट": "packet", "पैक": "packet",
    # Bottles
    "bottle": "bottle", "bottles": "bottle", "बोतल": "bottle",
    # Kilograms / Grams
    "kg": "kg", "kgs": "kg", "kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg", "किलो": "kg", "किग्रा": "kg",
    "g": "g", "gm": "g", "gms": "g", "gram": "g", "grams": "g", "ग्राम": "g",
    # Liters
    "l": "litre", "liter": "litre", "liters": "litre", "litre": "litre", "litres": "litre", "लीटर": "litre",
    "ml": "ml", "मिली": "ml",
    # Dozen
    "dozen": "dozen", "dozens": "dozen", "doz": "dozen", "दर्जन": "dozen",
    # Loaf
    "loaf": "loaf", "loaves": "loaf",
    # Box
    "box": "box", "boxes": "box", "डिब्बा": "box",
    # Can
    "can": "can", "cans": "can", "टिन": "can",
    # Pieces
    "piece": "piece", "pieces": "piece", "pc": "piece", "pcs": "piece", "नग": "piece", "पीस": "piece",
    # Bunch
    "bunch": "bunch", "bunches": "bunch", "गुच्छा": "bunch",
    # Cup / Tub / Bar
    "cup": "cup", "cups": "cup", "tub": "tub", "tubs": "tub", "bar": "bar", "bars": "bar",
    "tube": "tube", "tubes": "tube", "jar": "jar", "jars": "jar", "bag": "bag", "bags": "bag"
}

# Known Brands
KNOWN_BRANDS = [
    "amul", "tata", "britannia", "freshfarm", "organic india", "nestle", "coca cola", "coca-cola", "coke",
    "pepsi", "thums up", "colgate", "sensodyne", "surf excel", "vim", "lizol", "dettol", "dove", "modern",
    "daawat", "aashirvaad", "fortune", "madhur", "eggoz", "epigamia", "raw pressery", "sofit", "oatly",
    "lays", "lay's", "parle", "parle-g", "haldiram's", "haldiram", "cadbury", "real"
]

# Known Attributes
KNOWN_ATTRIBUTES = [
    "organic", "whole wheat", "multigrain", "brown", "toned", "full cream", "full-cream",
    "skimmed", "sugar-free", "gluten-free", "lactose-free", "plant-based", "vegan",
    "unpolished", "cold-pressed", "salted", "unsalted", "fresh", "diet", "zero"
]

# Common Hindi Stopwords & Grammar Particles in shopping requests
HINDI_VOCAB_MAP = {
    "doodh": "Milk", "dudh": "Milk", "दूध": "Milk",
    "chawal": "Rice", "चावल": "Rice",
    "seb": "Apple", "सेब": "Apple",
    "kela": "Banana", "kele": "Banana", "केला": "Banana", "केले": "Banana",
    "tamatar": "Tomato", "टमाटर": "Tomato",
    "pyaz": "Onion", "pyaaz": "Onion", "प्याज": "Onion",
    "aloo": "Potato", "alu": "Potato", "आलू": "Potato",
    "palak": "Spinach", "पालक": "Spinach",
    "cheeni": "Sugar", "chini": "Sugar", "चीनी": "Sugar",
    "shakkar": "Sugar", "शक्कर": "Sugar",
    "namak": "Salt", "नमक": "Salt",
    "atta": "Whole Wheat Flour", "aata": "Whole Wheat Flour", "आटा": "Whole Wheat Flour",
    "daal": "Dal", "दाल": "Dal",
    "tel": "Oil", "तेल": "Oil",
    "makhan": "Butter", "मक्खन": "Butter",
    "butter": "Butter","बटर": "Butter",
    "dahi": "Curd", "दही": "Curd",
    "paneer": "Paneer", "पनीर": "Paneer",
    "ande": "Eggs", "anda": "Egg", "अंडा": "Egg", "अंडे": "Eggs",
    "chai": "Tea", "चाय": "Tea",
    "biskut": "Biscuits", "biscuits": "Biscuits", "बिस्कुट": "Biscuits",
    "sabzi": "Vegetables", "sabji": "Vegetables", "सब्जी": "Vegetables"
}


def detect_language(text: str) -> str:
    """Detect whether input is English, Hindi (Devanagari), or Hinglish."""
    if any("\u0900" <= char <= "\u097f" for char in text):
        return "hi"

    hinglish_markers = [
        "karo", "kardo", "kar do", "chahiye", "daal do", "daalo", "hata do", "hatao",
        "nikal do", "nikalo", "khareed", "bhej", "doodh", "chawal", "cheeni", "namak",
        "seb", "kela", "aloo", "pyaz", "paani", "andar", "bhi", "mein", "aur",
        "dhoondho", "dikhao", "batao", "hai", "mujhe", "humko", "kripya", "zara", "mat"
    ]
    words = text.lower().split()
    if any(w in hinglish_markers for w in words) or any(m in text.lower() for m in ["kar do", "daal do", "hata do", "chahiye", "nikal do", "ke andar"]):
        return "hinglish"

    return "en"


def normalize_text(text: str) -> str:
    """Clean and normalize transcript text for consistent token matching."""
    cleaned = text.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip("\"'.,!?")
    return cleaned


def clean_sentence_preamble(text: str) -> str:
    """Strip conversational opening phrases."""
    p = re.sub(
        r"^(actually,?\s*|please,?\s*|can you,?\s*|could you,?\s*|i need\s+|i want\s+|i'd like\s+|i would like\s+|put\s+|add\s+|buy\s+|get me\s+|don't forget to buy\s+|don't forget\s+|dont forget\s+|mujhe\s+|humko\s+|kripya\s+|zara\s+|कृपया\s+|मुझे\s+)",
        "",
        text,
        flags=re.IGNORECASE
    )
    return p.strip()


def clean_sentence_postfix(text: str) -> str:
    """Strip conversational closing phrases."""
    p = re.sub(
    r"(?:add\s+kar\s*do|add\s+karo|ऐड\s+करो|ऐड\s+कर\s+दो|ऐड\s+कर|चाहिए|डाल\s+दो|जोड़\s+दो)$",
    "",
    text,
    flags=re.IGNORECASE
)
    return p.strip()


def parse_quantity_and_unit(phrase: str) -> Tuple[float, str, str]:
    """
    Extract quantity, unit and product name from English, Hindi and Hinglish
    shopping commands.

    Examples:
        '2 packets of Amul milk' -> (2, 'packet', 'Amul milk')
        'a loaf of bread' -> (1, 'loaf', 'bread')
        'do kilo chawal' -> (2, 'kg', 'rice')
        'do dudh ke packet add kar de' -> (2, 'packet', 'milk')
        'butter add kar de' -> (1, 'piece', 'butter')
    """

    phrase = clean_sentence_preamble(phrase)
    phrase = clean_sentence_postfix(phrase)

    words = phrase.split()

    if not words:
        return 1.0, "piece", phrase

    quantity = 1.0
    unit = "piece"
    idx = 0

    first_word = words[0].lower().strip(".,!?")

    # ---------------------------------------------------------
    # 1. Extract quantity
    # ---------------------------------------------------------
    if re.match(r"^\d+(\.\d+)?$", first_word):
        quantity = float(first_word)
        idx = 1

    elif first_word in NUMBER_WORDS:
        quantity = NUMBER_WORDS[first_word]
        idx = 1

    elif "/" in first_word:
        parts = first_word.split("/")
        if (
            len(parts) == 2
            and parts[0].isdigit()
            and parts[1].isdigit()
            and float(parts[1]) != 0
        ):
            quantity = float(parts[0]) / float(parts[1])
            idx = 1

    # ---------------------------------------------------------
    # 2. Extract unit
    # ---------------------------------------------------------
    if idx < len(words):
        current_word = words[idx].lower().rstrip(".,!?")

        # Direct unit:
        # "2 packets milk"
        # "2 kilo rice"
        if current_word in UNIT_MAP:
            unit = UNIT_MAP[current_word]
            idx += 1

            # Skip connector after unit:
            # "2 packets of milk"
            # "2 packets ke milk"
            if (
                idx < len(words)
                and words[idx].lower().rstrip(".,!?")
                in ["of", "ka", "ki", "ke", "का", "की", "के"]
            ):
                idx += 1

        # Connector before unit:
        # "do dudh ke packet"
        #             ^ packet
        elif current_word in ["ka", "ki", "ke", "का", "की", "के"]:
            connector_idx = idx

            if connector_idx + 1 < len(words):
                possible_unit = words[connector_idx + 1].lower().rstrip(".,!?")

                if possible_unit in UNIT_MAP:
                    unit = UNIT_MAP[possible_unit]
                    idx = connector_idx + 2

    # ---------------------------------------------------------
    # 3. Remove leading connectors
    # ---------------------------------------------------------
    remaining_product = " ".join(words[idx:]).strip()

    remaining_product = re.sub(
        r"^(of|some|any|a|an|the|ka|ki|ke|का|की|के)\s+",
        "",
        remaining_product,
        flags=re.IGNORECASE
    )

    # ---------------------------------------------------------
    # 4. Remove common Hinglish/Hindi command words
    #    from the END of the product phrase
    # ---------------------------------------------------------
    command_suffixes = [
        r"\s+add\s+kar\s+de$",
        r"\s+add\s+kar\s+do$",
        r"\s+add\s+karo$",
        r"\s+add\s+kr\s+de$",
        r"\s+add\s+kr\s+do$",
        r"\s+kar\s+de$",
        r"\s+kar\s+do$",
        r"\s+karo$",
        r"\s+जोड़\s+दे$",
        r"\s+जोड़\s+दो$",
        r"\s+जोड़\s+दीजिए$",
        r"\s+जोड़\s+दिया$",
        r"\s+जोड़\s+दो$",
        r"\s+ऐड\s+कर\s+दे$",
        r"\s+ऐड\s+कर\s+दो$",
        r"\s+jod\s+do$",
        r"\s+jod\s+de$"
    ]

    for suffix in command_suffixes:
        remaining_product = re.sub(
            suffix,
            "",
            remaining_product,
            flags=re.IGNORECASE
        )

    remaining_product = remaining_product.strip()

    # ---------------------------------------------------------
    # 5. Translate known Hindi grocery words
    # ---------------------------------------------------------
    prod_words = remaining_product.split()

    translated_words = [
    HINDI_VOCAB_MAP.get(
        w.lower(),
        HINDI_VOCAB_MAP.get(w, w)
    )
    for w in prod_words
]

    HINGLISH_MAP = {
    "makkhan": "butter",
    "makhan": "butter",
    "doodh": "milk",
    "dudh": "milk",
    "dahi": "curd",
    "chawal": "rice",
    "cheeni": "sugar",
    "chini": "sugar",
    "namak": "salt",
    "tel": "oil",
    "seb": "apple",
    "aam": "mango",
    "atta": "flour",
    "aata": "flour",
}

    translated_words = [
    HINGLISH_MAP.get(word.lower(), word)
    for word in translated_words
]

    standardized_product = " ".join(translated_words).strip()

    return quantity, unit, standardized_product

def extract_brand_and_attributes(product_str: str) -> Tuple[Optional[str], List[str], str]:
    """Extract known brands, attributes (organic, whole wheat, etc.) and clean product name."""
    lower = product_str.lower()
    detected_brand = None
    detected_attributes = []

    for brand in KNOWN_BRANDS:
        pattern = r"\b" + re.escape(brand) + r"\b"
        if re.search(pattern, lower):
            detected_brand = " ".join(w.capitalize() for w in brand.split())
            lower = re.sub(pattern, "", lower)
            break

    for attr in KNOWN_ATTRIBUTES:
        pattern = r"\b" + re.escape(attr) + r"\b"
        if re.search(pattern, lower):
            detected_attributes.append(attr)
            lower = re.sub(pattern, "", lower)

    cleaned_name = re.sub(r"\s+", " ", lower).strip()
    if not cleaned_name:
        cleaned_name = product_str.strip()

    return detected_brand, detected_attributes, cleaned_name.title()


def extract_price_limits(text: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract min and max price limits from queries."""
    min_price = None
    max_price = None

    between_match = re.search(r"(?:between|range)\s*(?:₹|rs\.?|rupees)?\s*(\d+)\s*(?:and|to|-)\s*(?:₹|rs\.?|rupees)?\s*(\d+)", text, re.IGNORECASE)
    if not between_match:
        between_match = re.search(r"(\d+)\s*(?:se|to|-)\s*(\d+)\s*(?:tak|rupaye|rupees)?", text, re.IGNORECASE)

    if between_match:
        val1 = float(between_match.group(1))
        val2 = float(between_match.group(2))
        return min(val1, val2), max(val1, val2)

    max_match = re.search(r"(?:under|below|less than|upto|up to|max|maximum|within)\s*(?:₹|rs\.?|rupees)?\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if not max_match:
        max_match = re.search(r"(?:₹|rs\.?|rupees)?\s*(\d+(?:\.\d+)?)\s*(?:rupaye|rupees)?\s*(?:ke\s*andar|tak|se\s*kam|below|under)", text, re.IGNORECASE)

    if max_match:
        max_price = float(max_match.group(1))

    min_match = re.search(r"(?:above|over|more than|min|minimum)\s*(?:₹|rs\.?|rupees)?\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if not min_match:
        min_match = re.search(r"(?:₹|rs\.?|rupees)?\s*(\d+(?:\.\d+)?)\s*(?:rupaye|rupees)?\s*(?:se\s*zyada|above)", text, re.IGNORECASE)

    if min_match:
        min_price = float(min_match.group(1))

    return min_price, max_price


def split_multi_items(text: str) -> List[str]:
    """Split complex multi-item sentences."""
    cleaned = clean_sentence_preamble(text)
    cleaned = clean_sentence_postfix(cleaned)

    parts = re.split(r",\s*(?:and\s+|aur\s+|tatha\s+|&\s+)?|\s+(?:and|aur|tatha|&)\s+", cleaned, flags=re.IGNORECASE)
    items = [p.strip() for p in parts if p.strip()]
    return items if items else [text]


def parse_command(raw_text: str, language_hint: str = "auto") -> Dict[str, Any]:
    """Main Natural Language Parsing Pipeline."""
    normalized = normalize_text(raw_text)
    detected_lang = detect_language(normalized) if language_hint == "auto" else language_hint
    lower = normalized.lower()

    intent = "UNKNOWN"
    confidence = 0.95
    reasoning = ""
    entities: Dict[str, Any] = {}
    action_executed = "NOOP"
    confirmation_message = ""
    tts_text = ""

    # =========================================================================
    # 1. INTENT: CLEAR_LIST / CLEAR_PURCHASED
    # =========================================================================
    if any(k in lower for k in ["clear purchased", "remove bought", "delete purchased", "khareede hue items hata", "bought items hata"]):
        intent = "CLEAR_PURCHASED"
        reasoning = "Matched 'clear purchased' pattern to clean up marked off grocery items."
        action_executed = "CLEAR_PURCHASED_ITEMS"
        confirmation_message = "Cleared all purchased items from your list."
        tts_text = "Purchased items have been cleared."

    elif any(k in lower for k in [
        "clear my list", "clear list", "clear shopping list", "delete everything", "empty cart",
        "empty list", "clear cart", "saari list clear", "sab hata do", "poori list saaf"
    ]):
        intent = "CLEAR_LIST"
        reasoning = "Matched command for resetting the active shopping list."
        action_executed = "CLEAR_ENTIRE_LIST"
        confirmation_message = "Shopping list cleared."
        tts_text = "Your shopping list has been cleared."

    # =========================================================================
    # 2. INTENT: UNDO
    # =========================================================================
    elif any(k in lower for k in ["undo", "undo last", "revert", "piche lo", "vapas karo", "undo action"]):
        intent = "UNDO"
        reasoning = "Matched undo request to revert the previous mutation."
        action_executed = "UNDO_LAST_ACTION"
        confirmation_message = "Undid the last action."
        tts_text = "Reverted last action."

    # =========================================================================
    # 3. INTENT: REMOVE_ITEM (Checked before generic to avoid number collision with 'hata do')
    # =========================================================================
    elif (
        any(k in lower for k in [
            "remove", "delete", "hata do", "hatao", "nikal do", "nikalo", "cancel", "cancel karo", "mat lo", "हटा दो", "निकाल दो"
        ])
        or ("take" in lower and "off" in lower)
        or ("don't need" in lower or "dont need" in lower)
    ) and not any(k in lower for k in ["clear purchased", "clear list", "clear my"]):
        intent = "REMOVE_ITEM"
        target = re.sub(r"^(please\s+|can\s+you\s+|remove\s+|delete\s+|take\s+|i\s+don't\s+need\s+|i\s+dont\s+need\s+|cancel\s+)", "", lower)
        target = re.sub(r"\s+(off\s+my\s+list|off\s+the\s+list|from\s+my\s+list|from\s+the\s+list|off|anymore|hata\s*do|hatao|nikal\s*do|nikalo|cancel\s*karo|mat\s*lo|हटा\s*दो|निकाल\s*दो)$", "", target).strip()
        target = re.sub(r"^(the|a|an|some)\s+", "", target).strip()

        words = [HINDI_VOCAB_MAP.get(w, w) for w in target.split()]
        target_clean = " ".join(words).title()

        entities = {
            "product": target_clean
        }
        reasoning = f"Extracted item deletion command for '{target_clean}'."
        action_executed = "REMOVE_FROM_SHOPPING_LIST"
        confirmation_message = f"Removed '{target_clean}' from your shopping list."
        tts_text = f"Removed {target_clean} from your shopping list."

    # =========================================================================
    # 4. INTENT: UPDATE_QUANTITY
    # =========================================================================
    elif any(k in lower for k in ["make that", "actually, make that", "actually make that", "change", "update quantity", "kar do"]) and any(
        re.search(r"\b" + re.escape(num) + r"\b", lower) or re.search(r"\d+", lower)
        for num in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "1", "2", "3", "4", "5"]
    ) and not lower.startswith(("add", "put", "buy", "daal")):
        intent = "UPDATE_QUANTITY"
        clean_text = re.sub(r"^(actually,?\s*make\s+that\s+|actually,?\s*make\s+|make\s+that\s+|make\s+|change\s+|update\s+)", "", lower)
        clean_text = re.sub(r"\s+(kar\s*do|karo)$", "", clean_text).strip()

        qty, unit, prod = parse_quantity_and_unit(clean_text)
        if " to " in clean_text:
            p_part, q_part = clean_text.split(" to ", 1)
            qty, unit, _ = parse_quantity_and_unit(q_part)
            prod = p_part.strip().title()

        brand, attrs, prod_name = extract_brand_and_attributes(prod)

        entities = {
            "product": prod_name,
            "quantity": qty,
            "unit": unit,
            "brand": brand
        }
        reasoning = f"Parsed update quantity request: set quantity to {qty} {unit} for '{prod_name}'."
        action_executed = "UPDATE_ITEM_QUANTITY"
        confirmation_message = f"Updated '{prod_name}' to {qty:g} {unit}."
        tts_text = f"Updated {prod_name} to {qty:g} {unit}."

    # =========================================================================
    # 5. INTENT: SHOW_LIST
    # =========================================================================
    elif any(k in lower for k in [
        "show list", "show my list", "show shopping list", "what do i have", "what do i still need",
        "what's on my list", "whats on my list", "view list", "list dikhao", "kya khareedna hai",
        "meri list batao", "list mein kya hai"
    ]):
        intent = "SHOW_LIST"
        reasoning = "User is requesting to view their current shopping checklist."
        action_executed = "RETRIEVE_SHOPPING_LIST"
        confirmation_message = "Here is your current shopping list."
        tts_text = "Here is what you currently have on your shopping list."

    # =========================================================================
    # 6. INTENT: GET_RECOMMENDATIONS
    # =========================================================================
    elif any(k in lower for k in [
        "what should i buy", "what do i usually buy", "what am i missing", "going grocery shopping",
        "recommend", "suggestions", "kya khareedna chahiye", "kya miss ho raha hai", "suggest karo"
    ]):
        intent = "GET_RECOMMENDATIONS"
        reasoning = "User requested intelligent shopping recommendations based on historical buying cycle."
        action_executed = "FETCH_RECOMMENDATIONS"
        confirmation_message = "Generated personalized smart recommendations."
        tts_text = "Here are your personalized suggestions based on your usual shopping frequency."

    # =========================================================================
    # 7. INTENT: SEARCH_PRODUCT / PRICE LIMIT
    # =========================================================================
    elif any(k in lower for k in ["find", "search", "show me", "look for", "dhoondho", "khojo", "ढूंढो"]) and any(
        k in lower for k in ["under", "below", "price", "rupees", "rs", "₹", "organic", "brand", "shampoo", "toothpaste", "biscuits", "apples", "salt", "oil", "tak", "andar", "के अंदर"]
    ) or lower.startswith(("find ", "search ", "look for ", "dhoondho ", "khojo ")):
        intent = "SEARCH_PRODUCT"
        min_p, max_p = extract_price_limits(lower)

        clean_q = re.sub(r"^(find|search|show me|look for|dhoondho|khojo|ढूंढो)\s+", "", lower)
        clean_q = re.sub(r"(?:under|below|less than|between|range|within|upto|above)\s*(?:₹|rs\.?|rupees)?\s*\d+(\s*(?:and|to|-)\s*\d+)?.*$", "", clean_q)
        clean_q = re.sub(r"\s*\d+\s*(?:rupaye|rupees)?\s*(?:ke\s*andar|tak|se\s*kam|se\s*zyada|के\s*अंदर).*$", "", clean_q)
        clean_q = clean_q.strip()

        brand, attrs, final_product = extract_brand_and_attributes(clean_q)

        # Map Hindi words in search if present
        s_words = [HINDI_VOCAB_MAP.get(w.lower(), w) for w in final_product.split()]
        final_query = " ".join(s_words).title() if s_words else clean_q.title()

        entities = {
            "query": final_query,
            "product": final_query,
            "brand": brand,
            "attributes": attrs,
            "min_price": min_p,
            "max_price": max_p
        }
        reasoning = f"Parsed search intent for '{final_query}' with price bounds: min={min_p}, max={max_p}, brand={brand}, attributes={attrs}."
        action_executed = "SEARCH_CATALOG"
        confirmation_message = f"Found matching products for '{final_query}'."
        tts_text = f"Searching for {final_query}."

    # =========================================================================
    # 8. INTENT: MARK_PURCHASED (Shopping Mode / In-Store)
    # =========================================================================
    elif any(k in lower for k in [
        "bought", "i've bought", "ive bought", "purchased", "mark as bought", "mark as purchased",
        "khareed liya", "le liya", "done with", "tick kar do", "tick karo", "got the", "mark done"
    ]):
        intent = "MARK_PURCHASED"
        target = re.sub(r"^(i've\s+bought|ive\s+bought|i\s+bought|bought|purchased|mark\s+|got\s+(the\s+)?|maine\s+)", "", lower)
        target = re.sub(r"\s+(as\s+bought|as\s+purchased|done|khareed\s*liya|le\s*liya|tick\s*karo|tick\s*kar\s*do)$", "", target).strip()
        target = re.sub(r"^(the|a|an)\s+", "", target).strip()

        words = [HINDI_VOCAB_MAP.get(w, w) for w in target.split()]
        target_clean = " ".join(words).title()

        entities = {
            "product": target_clean,
            "status": "purchased"
        }
        reasoning = f"Detected in-store purchase confirmation for item: '{target_clean}'."
        action_executed = "MARK_ITEM_PURCHASED"
        confirmation_message = f"Marked '{target_clean}' as purchased."
        tts_text = f"{target_clean} marked as purchased."

    # =========================================================================
    # 9. INTENT: HELP
    # =========================================================================
    elif lower in ["help", "what can you do", "commands", "madad", "kaise use kare", "help me"]:
        intent = "HELP"
        reasoning = "User requested help instructions."
        action_executed = "SHOW_HELP"
        confirmation_message = "You can speak naturally: 'Add 2 packets of milk', 'Remove bread', 'Find organic apples under ₹300', or 'What should I buy?'"
        tts_text = "You can add or remove items, search products with price filters, or ask for recommendations."

    # =========================================================================
    # 10. INTENT: ADD_ITEMS (Default for item mentions or explicit add commands)
    # =========================================================================
    else:
        intent = "ADD_ITEMS"
        item_phrases = split_multi_items(normalized)
        extracted_items = []

        for phrase in item_phrases:
            qty, unit, prod_raw = parse_quantity_and_unit(phrase)
            brand, attrs, prod_name = extract_brand_and_attributes(prod_raw)
            category = classify_category(prod_name, brand)
            estimated_price = estimate_item_price(prod_name, brand, qty)

            extracted_items.append({
                "name": prod_name if prod_name else phrase.title(),
                "quantity": qty,
                "unit": unit,
                "brand": brand,
                "category": category,
                "attributes": attrs,
                "estimated_price": estimated_price
            })

        entities = {
            "items": extracted_items,
            "total_items_detected": len(extracted_items)
        }

        if len(extracted_items) == 1:
            item = extracted_items[0]
            brand_str = f"{item['brand']} " if item.get("brand") else ""
            item_desc = f"{item['quantity']:g} {item['unit']}{'s' if item['quantity'] > 1 and not item['unit'].endswith('s') else ''} of {brand_str}{item['name']}"
            reasoning = f"Parsed single item addition: {item_desc} in '{item['category']}' category."
            if detected_lang == "hi":
                confirmation_message = (
        f"{item['quantity']:g} {item['unit']} {item['name']} जोड़ दिया।"
    )
                tts_text = confirmation_message

            elif detected_lang == "hinglish":
                confirmation_message = (
        f"{item['quantity']:g} {item['unit']} {item['name']} add kar diya."
    )
                tts_text = confirmation_message

            else:
                confirmation_message = f"Added {item_desc} to your shopping list."
                tts_text = f"Added {item_desc}."
        else:
            items_desc = ", ".join([f"{it['quantity']:g} {it['name']}" for it in extracted_items])
            reasoning = f"Parsed multi-item addition ({len(extracted_items)} items): {items_desc}."
            confirmation_message = f"Added {len(extracted_items)} items: {items_desc} to your shopping list."
            tts_text = f"Added {len(extracted_items)} items to your list."

        action_executed = "ADD_TO_SHOPPING_LIST"

    pipeline = {
        "raw_transcript": raw_text,
        "normalized_text": normalized,
        "detected_language": detected_lang,
        "intent": intent,
        "confidence": confidence,
        "entities": entities,
        "reasoning": reasoning,
        "action_executed": action_executed,
        "confirmation_message": confirmation_message,
        "tts_text": tts_text
    }

    return {
        "intent": intent,
        "entities": entities,
        "reasoning": reasoning,
        "action_executed": action_executed,
        "confirmation_message": confirmation_message,
        "tts_text": tts_text,
        "pipeline": pipeline
    }


def estimate_item_price(product_name: str, brand: Optional[str], quantity: float) -> Optional[float]:
    """Estimate item price based on product name and brand."""
    from app.services.product_catalog_data import CATALOG_PRODUCTS

    target = product_name.lower()
    for p in CATALOG_PRODUCTS:
        p_name = p["name"].lower()
        if brand and p.get("brand") and brand.lower() in p["brand"].lower() and target in p_name:
            return round(p["price"] * quantity, 2)
        if target in p_name or p_name in target:
            return round(p["price"] * quantity, 2)

    cat = classify_category(product_name, brand)
    defaults = {
        "Dairy": 40.0,
        "Produce": 50.0,
        "Bakery": 45.0,
        "Beverages": 60.0,
        "Snacks": 35.0,
        "Pantry": 120.0,
        "Meat": 150.0,
        "Personal Care": 120.0,
        "Household": 140.0
    }
    base = defaults.get(cat, 50.0)
    return round(base * quantity, 2)
