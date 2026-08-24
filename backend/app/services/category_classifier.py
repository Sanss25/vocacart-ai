"""
Category Classifier with comprehensive dictionary and rule-based heuristic fallback.
Categories:
- Produce
- Dairy
- Meat
- Bakery
- Beverages
- Snacks
- Frozen
- Household
- Personal Care
- Pantry
- Other
"""

CATEGORY_DICTIONARY = {
    "Produce": [
        # Fruits
        "apple", "apples", "banana", "bananas", "orange", "oranges", "mango", "mangoes", "grape", "grapes",
        "watermelon", "papaya", "pomegranate", "lemon", "lemons", "lime", "limes", "strawberry", "strawberries",
        "blueberry", "blueberries", "avocado", "guava", "pineapple", "kiwi", "pear", "pears", "plum", "plums",
        "coconut", "peach", "peaches", "cherry", "cherries", "muskmelon", "custard apple",
        # Vegetables
        "tomato", "tomatoes", "potato", "potatoes", "onion", "onions", "garlic", "ginger", "spinach", "palak",
        "coriander", "cilantro", "mint", "pudina", "carrot", "carrots", "broccoli", "cauliflower", "gobi",
        "cabbage", "patta gobi", "capsicum", "bell pepper", "shimla mirch", "cucumber", "kheera", "eggplant",
        "brinjal", "baingan", "ladyfinger", "okra", "bhindi", "peas", "matar", "green peas", "mushroom",
        "mushrooms", "bottle gourd", "lauki", "bitter gourd", "karela", "pumpkin", "kaddu", "radish", "mooli",
        "beetroot", "zucchini", "lettuce", "chili", "chilies", "green chili", "hari mirch", "methi", "fenugreek",
        # Hindi terms
        "seb", "kela", "aam", "santra", "angoor", "anar", "nimbu", "alu", "aloo", "tamatar", "pyaz", "pyaaz",
        "adrak", "lahsun", "lasun", "sabzi", "sabji", "tarkari"
    ],
    "Dairy": [
        "milk", "doodh", "curd", "dahi", "yogurt", "yoghurt", "greek yogurt", "paneer", "cottage cheese",
        "cheese", "cheddar", "mozzarella", "parmesan", "butter", "makhan", "ghee", "clarified butter",
        "cream", "malai", "heavy cream", "whipping cream", "sour cream", "buttermilk", "chaas", "lassi",
        "condensed milk", "milk powder", "almond milk", "soy milk", "oat milk", "coconut milk", "tofu"
    ],
    "Bakery": [
        "bread", "white bread", "brown bread", "whole wheat bread", "multigrain bread", "sourdough", "pav",
        "buns", "burger buns", "hot dog buns", "croissant", "bagel", "bagels", "muffin", "muffins", "cake",
        "pastry", "pastries", "donut", "donuts", "doughnut", "doughnuts", "pita bread", "tortilla", "roti",
        "paratha", "naan", "kulcha", "rusk", "toast", "pao"
    ],
    "Beverages": [
        "tea", "chai", "green tea", "black tea", "coffee", "cold coffee", "instant coffee", "filter coffee",
        "juice", "orange juice", "apple juice", "mango juice", "soft drink", "coke", "coca cola", "pepsi",
        "thums up", "sprite", "fanta", "limca", "soda", "sparkling water", "tonic water", "energy drink",
        "red bull", "water", "mineral water", "packaged water", "paani", "squash", "syrup", "rooh afza"
    ],
    "Snacks": [
        "chips", "potato chips", "lays", "doritos", "nachos", "popcorn", "biscuits", "biscuit", "cookies",
        "cookie", "parle-g", "oreo", "bourbon", "good day", "rusk", "namkeen", "bhujia", "sev", "mixture",
        "kurkure", "chocolate", "chocolates", "cadbury", "kitkat", "munch", "dairy milk", "candy", "gum",
        "nuts", "cashews", "almonds", "badam", "kaju", "peanuts", "mungfali", "walnuts", "akhrot", "pistachios",
        "pista", "raisins", "kishmish", "makhana", "fox nuts", "roasted chana", "wafer", "wafers"
    ],
    "Pantry": [
        "rice", "chawal", "basmati rice", "brown rice", "flour", "atta", "wheat flour", "maida", "besan",
        "gram flour", "sooji", "suji", "rava", "semolina", "dal", "daal", "lentils", "toor dal", "moong dal",
        "chana dal", "urad dal", "masoor dal", "rajma", "kidney beans", "chole", "chickpeas", "kabuli chana",
        "sugar", "cheeni", "shakkar", "jaggery", "gud", "salt", "namak", "rock salt", "black salt", "oil",
        "tel", "sunflower oil", "mustard oil", "sarson tel", "olive oil", "vegetable oil", "coconut oil",
        "spices", "masala", "turmeric", "haldi", "red chili powder", "lal mirch", "coriander powder", "dhaniya powder",
        "cumin", "jeera", "garam masala", "mustard seeds", "rai", "cardamom", "elaichi", "cloves", "laung",
        "cinnamon", "dalchini", "black pepper", "kali mirch", "pasta", "noodles", "maggie", "maggi", "sauce",
        "ketchup", "tomato ketchup", "soya sauce", "mayonnaise", "mayo", "vinegar", "honey", "jam", "peanut butter",
        "pickle", "achar"
    ],
    "Meat": [
        "chicken", "chicken breast", "mutton", "lamb", "goat meat", "fish", "prawns", "shrimp", "salmon",
        "tuna", "pork", "bacon", "sausage", "sausages", "ham", "salami", "egg", "eggs", "anda", "ande"
    ],
    "Frozen": [
        "frozen peas", "frozen corn", "ice cream", "kulfi", "frozen french fries", "frozen nuggets",
        "frozen burger patties", "frozen paratha", "frozen pizza", "frozen berries", "popsicles", "ice"
    ],
    "Household": [
        "detergent", "surf excel", "ariel", "tide", "dishwash liquid", "vim", "pril", "scrubber", "sponge",
        "floor cleaner", "lizol", "toilet cleaner", "harpic", "glass cleaner", "colin", "trash bags",
        "garbage bags", "aluminum foil", "foil", "cling wrap", "tissue", "tissue paper", "kitchen roll",
        "paper towels", "napkins", "mop", "broom", "broomstick", "mosquito repellent", "good knight", "all out",
        "air freshener", "odonil", "matchbox", "candles", "batteries", "light bulb"
    ],
    "Personal Care": [
        "soap", "bath soap", "body wash", "shower gel", "shampoo", "conditioner", "face wash", "toothpaste",
        "dant manjan", "colgate", "sensodyne", "pepsodent", "toothbrush", "mouthwash", "deodorant", "perfume",
        "deo", "hand wash", "sanitizer", "hand sanitizer", "body lotion", "moisturizer", "sunscreen", "cold cream",
        "hair oil", "coconut hair oil", "shaving cream", "razor", "razor blades", "cotton", "cotton buds",
        "sanitary pads", "tampons", "diapers", "baby wipes", "lip balm"
    ]
}


def classify_category(product_name: str, brand: str = None) -> str:
    """
    Classify a product into one of the standard supermarket categories.
    Uses direct dictionary matching, substring matching, and keyword heuristics.
    """
    if not product_name:
        return "Other"

    text = product_name.lower().strip()
    if brand:
        text = f"{brand.lower()} {text}"

    # 1. Exact match in category dictionary
    for category, items in CATEGORY_DICTIONARY.items():
        for item in items:
            if text == item:
                return category

    # 2. Tokenized word boundary or phrase match
    words = text.split()
    for category, items in CATEGORY_DICTIONARY.items():
        for item in items:
            # check if entire item phrase is in text
            if f" {item} " in f" {text} " or text.startswith(f"{item} ") or text.endswith(f" {item}"):
                return category

    # 3. Substring matching for distinctive terms
    for category, items in CATEGORY_DICTIONARY.items():
        for item in items:
            if len(item) >= 4 and item in text:
                return category

    # 4. Fallback heuristics
    if any(k in text for k in ["wash", "soap", "cream", "paste", "brush", "gel", "lotion", "shampoo", "perfume", "deodorant"]):
        return "Personal Care"
    if any(k in text for k in ["cleaner", "detergent", "foil", "tissue", "bag", "mop", "bulb", "spray"]):
        return "Household"
    if any(k in text for k in ["fruit", "vegetable", "berry", "melon", "green", "fresh"]):
        return "Produce"
    if any(k in text for k in ["oil", "flour", "grain", "spice", "powder", "bean", "dal", "seed", "sauce"]):
        return "Pantry"
    if any(k in text for k in ["drink", "juice", "soda", "coffee", "tea", "water"]):
        return "Beverages"
    if any(k in text for k in ["snack", "chip", "biscuit", "chocolate", "nut", "cookie"]):
        return "Snacks"

    return "Other"
