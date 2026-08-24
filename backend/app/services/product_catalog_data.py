"""
Seed catalog data with 45+ products, Indian and global brands, price points in INR,
availability statuses (including out-of-stock items for substitute demonstrations),
and seasonal categories.
"""

CATALOG_PRODUCTS = [
    # Produce
    {
        "name": "Fresh Shimla Apples",
        "hindi_name": "ताजा शिमला सेब",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 180.0,
        "unit": "kg",
        "attributes": ["fresh", "sweet", "local"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=200&auto=format&fit=crop&q=80",
        "description": "Crisp and juicy hand-picked apples from Shimla orchards."
    },
    {
        "name": "Organic Royal Gala Apples",
        "hindi_name": "ऑर्गेनिक सेब",
        "brand": "Organic India",
        "category": "Produce",
        "price": 260.0,
        "unit": "kg",
        "attributes": ["organic", "pesticide-free", "premium"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?w=200&auto=format&fit=crop&q=80",
        "description": "Certified 100% organic Gala apples with naturally sweet flavor."
    },
    {
        "name": "Organic Strawberries",
        "hindi_name": "ऑर्गेनिक स्ट्रॉबेरी",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 280.0,
        "unit": "box",
        "attributes": ["organic", "seasonal", "sweet"],
        "availability": False,  # Out of stock for substitute demo
        "image_url": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=200&auto=format&fit=crop&q=80",
        "description": "Hand-picked organic sweet strawberries."
    },
    {
        "name": "Fresh Robusta Bananas",
        "hindi_name": "केले",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 60.0,
        "unit": "dozen",
        "attributes": ["fresh", "energy-rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=200&auto=format&fit=crop&q=80",
        "description": "Naturally ripened sweet bananas packed with potassium."
    },
    {
        "name": "Fresh Hybrid Tomatoes",
        "hindi_name": "ताजा टमाटर",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 40.0,
        "unit": "kg",
        "attributes": ["fresh", "juicy"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1546470427-e26264be0b11?w=200&auto=format&fit=crop&q=80",
        "description": "Firm red tomatoes perfect for salads, curries and sauces."
    },
    {
        "name": "Nashik Red Onions",
        "hindi_name": "नासिक लाल प्याज",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 35.0,
        "unit": "kg",
        "attributes": ["fresh", "pungent"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1508747703725-719777637510?w=200&auto=format&fit=crop&q=80",
        "description": "Quality pungent red onions sourced directly from Nashik."
    },
    {
        "name": "Farm Fresh Potatoes (Aloo)",
        "hindi_name": "आलू",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 30.0,
        "unit": "kg",
        "attributes": ["fresh", "staple"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=200&auto=format&fit=crop&q=80",
        "description": "Medium-sized smooth potatoes ideal for baking, boiling and frying."
    },
    {
        "name": "Fresh Green Spinach (Palak)",
        "hindi_name": "पालक",
        "brand": "FreshFarm",
        "category": "Produce",
        "price": 25.0,
        "unit": "bunch",
        "attributes": ["fresh", "leafy", "iron-rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=200&auto=format&fit=crop&q=80",
        "description": "Tender crisp spinach leaves washed and tied."
    },

    # Dairy
    {
        "name": "Amul Taaza Toned Milk",
        "hindi_name": "अमूल ताजा टोंड दूध",
        "brand": "Amul",
        "category": "Dairy",
        "price": 30.0,
        "unit": "packet",
        "attributes": ["toned", "pasteurized", "homogenized"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80",
        "description": "Amul Taaza pasteurized toned milk pouch (500ml)."
    },
    {
        "name": "Amul Gold Full Cream Milk",
        "hindi_name": "अमूल गोल्ड फुल क्रीम दूध",
        "brand": "Amul",
        "category": "Dairy",
        "price": 36.0,
        "unit": "packet",
        "attributes": ["full-cream", "pasteurized", "rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=200&auto=format&fit=crop&q=80",
        "description": "Rich full cream pasteurized milk for teas, desserts and direct consumption."
    },
    {
        "name": "Regular Cow Milk 1L",
        "hindi_name": "गाय का सादा दूध",
        "brand": "Mother Dairy",
        "category": "Dairy",
        "price": 65.0,
        "unit": "bottle",
        "attributes": ["cow milk", "pure"],
        "availability": False,  # Out of stock for substitute demo
        "image_url": "https://images.unsplash.com/photo-1528750997573-59b89d56f4f7?w=200&auto=format&fit=crop&q=80",
        "description": "Pure farm cow milk in 1L bottle."
    },
    {
        "name": "Raw Pressery Almond Milk Unsweetened",
        "hindi_name": "बादाम का दूध",
        "brand": "Raw Pressery",
        "category": "Dairy",
        "price": 180.0,
        "unit": "bottle",
        "attributes": ["plant-based", "lactose-free", "unsweetened", "vegan", "dairy-free"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1568651313337-b4d45544d6db?w=200&auto=format&fit=crop&q=80",
        "description": "Rich creamy almond milk made from premium California almonds."
    },
    {
        "name": "Sofit Soy Milk Chocolate Flavored",
        "hindi_name": "सोया दूध",
        "brand": "Sofit",
        "category": "Dairy",
        "price": 140.0,
        "unit": "bottle",
        "attributes": ["plant-based", "protein-rich", "dairy-free"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1588710929895-5cb95e68340e?w=200&auto=format&fit=crop&q=80",
        "description": "Enriched soy milk beverage with chocolate indulgence."
    },
    {
        "name": "Oatly Oat Milk Barista Edition",
        "hindi_name": "ओट मिल्क",
        "brand": "Oatly",
        "category": "Dairy",
        "price": 220.0,
        "unit": "bottle",
        "attributes": ["plant-based", "creamy", "vegan"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?w=200&auto=format&fit=crop&q=80",
        "description": "Creamy oat beverage crafted for coffee and tea foaming."
    },
    {
        "name": "Amul Salted Butter 100g",
        "hindi_name": "अमूल मक्खन",
        "brand": "Amul",
        "category": "Dairy",
        "price": 58.0,
        "unit": "packet",
        "attributes": ["salted", "classic"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=200&auto=format&fit=crop&q=80",
        "description": "The quintessential utterly butterly delicious Amul Butter."
    },
    {
        "name": "Amul Fresh Malai Paneer 200g",
        "hindi_name": "अमूल मलाई पनीर",
        "brand": "Amul",
        "category": "Dairy",
        "price": 92.0,
        "unit": "pack",
        "attributes": ["fresh", "soft", "protein-rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=200&auto=format&fit=crop&q=80",
        "description": "Soft and succulent cottage cheese made from pasteurized milk."
    },
    {
        "name": "Epigamia Greek Yogurt Natural",
        "hindi_name": "ग्रीक योगर्ट",
        "brand": "Epigamia",
        "category": "Dairy",
        "price": 60.0,
        "unit": "cup",
        "attributes": ["high-protein", "probiotic", "natural"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=200&auto=format&fit=crop&q=80",
        "description": "Strained thick Greek yogurt with zero preservatives."
    },

    # Bakery
    {
        "name": "Britannia 100% Whole Wheat Bread",
        "hindi_name": "ब्रिटानिया आटा ब्रेड",
        "brand": "Britannia",
        "category": "Bakery",
        "price": 55.0,
        "unit": "loaf",
        "attributes": ["whole wheat", "atta", "fiber-rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=200&auto=format&fit=crop&q=80",
        "description": "Soft brown loaf baked with 100% whole wheat flour."
    },
    {
        "name": "Classic White Bread",
        "hindi_name": "सफेद ब्रेड",
        "brand": "Modern",
        "category": "Bakery",
        "price": 40.0,
        "unit": "loaf",
        "attributes": ["soft", "sandwich"],
        "availability": False,  # Out of stock for substitute demo
        "image_url": "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=200&auto=format&fit=crop&q=80",
        "description": "Classic white sliced bread for daily breakfast sandwiches."
    },
    {
        "name": "The English Bakery Multigrain Bread",
        "hindi_name": "मल्टीग्रेन ब्रेड",
        "brand": "The English Bakery",
        "category": "Bakery",
        "price": 65.0,
        "unit": "loaf",
        "attributes": ["multigrain", "seeds", "healthy"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=200&auto=format&fit=crop&q=80",
        "description": "Wholesome multigrain loaf topped with flaxseeds and oats."
    },
    {
        "name": "Fresh Mumbai Pav (Pack of 6)",
        "hindi_name": "पाव",
        "brand": "Local Bakery",
        "category": "Bakery",
        "price": 30.0,
        "unit": "packet",
        "attributes": ["freshly-baked", "soft"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?w=200&auto=format&fit=crop&q=80",
        "description": "Fluffy oven fresh pav buns ideal for Pav Bhaji or Vada Pav."
    },

    # Pantry & Staples
    {
        "name": "Tata Salt Vacuum Evaporated 1kg",
        "hindi_name": "टाटा नमक",
        "brand": "Tata",
        "category": "Pantry",
        "price": 28.0,
        "unit": "packet",
        "attributes": ["iodized", "vacuum-evaporated", "staple"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1518110925495-5fe2fda0442c?w=200&auto=format&fit=crop&q=80",
        "description": "Desh ka namak - pure vacuum evaporated iodized salt."
    },
    {
        "name": "Aashirvaad Shudh Chakki Atta 5kg",
        "hindi_name": "आशीर्वाद शुद्ध चक्की आटा",
        "brand": "Aashirvaad",
        "category": "Pantry",
        "price": 245.0,
        "unit": "bag",
        "attributes": ["whole wheat", "chakki fresh", "fiber"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=200&auto=format&fit=crop&q=80",
        "description": "100% pure whole wheat flour for soft and fluffy rotis."
    },
    {
        "name": "Daawat Rozana Super Basmati Rice 5kg",
        "hindi_name": "दावत बासमती चावल",
        "brand": "Daawat",
        "category": "Pantry",
        "price": 395.0,
        "unit": "bag",
        "attributes": ["basmati", "long-grain", "aromatic"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&auto=format&fit=crop&q=80",
        "description": "Aromatic long grain basmati rice for everyday family dining."
    },
    {
        "name": "Tata Sampann Unpolished Toor Dal 1kg",
        "hindi_name": "टाटा संपन्न तूर दाल",
        "brand": "Tata Sampann",
        "category": "Pantry",
        "price": 175.0,
        "unit": "packet",
        "attributes": ["unpolished", "protein-rich", "pure"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1585994192701-f1a505c817ea?w=200&auto=format&fit=crop&q=80",
        "description": "Unpolished nutritious pigeon peas without water, oil or stone polishing."
    },
    {
        "name": "Fortune Sunlite Refined Sunflower Oil 1L",
        "hindi_name": "फॉर्च्यून सनफ्लावर तेल",
        "brand": "Fortune",
        "category": "Pantry",
        "price": 145.0,
        "unit": "pouch",
        "attributes": ["refined", "light", "heart-healthy"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=200&auto=format&fit=crop&q=80",
        "description": "Light, healthy and easy-to-digest refined sunflower cooking oil."
    },
    {
        "name": "Madhur Pure & Hygienic Sugar 1kg",
        "hindi_name": "मधुर चीनी",
        "brand": "Madhur",
        "category": "Pantry",
        "price": 52.0,
        "unit": "packet",
        "attributes": ["sulfur-free", "refined", "hygienic"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1622484216278-831e5bb8266c?w=200&auto=format&fit=crop&q=80",
        "description": "100% sulfur-free refined sparkling crystal sugar."
    },
    {
        "name": "Maggi 2-Minute Masala Noodles (Pack of 4)",
        "hindi_name": "मैगी मसाला नूडल्स",
        "brand": "Nestle",
        "category": "Pantry",
        "price": 56.0,
        "unit": "packet",
        "attributes": ["instant", "masala", "quick"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=200&auto=format&fit=crop&q=80",
        "description": "India's favorite instant noodles infused with roasted spices."
    },

    # Beverages
    {
        "name": "Tata Tea Gold 500g",
        "hindi_name": "टाटा टी गोल्ड चाय",
        "brand": "Tata",
        "category": "Beverages",
        "price": 290.0,
        "unit": "packet",
        "attributes": ["aromatic", "rich blend", "assorted leaves"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=200&auto=format&fit=crop&q=80",
        "description": "Exquisite blend of strong Assam CTC teas and gently rolled long tea leaves."
    },
    {
        "name": "Nescafe Classic Instant Coffee 100g",
        "hindi_name": "नेस्कैफे कॉफी",
        "brand": "Nestle",
        "category": "Beverages",
        "price": 310.0,
        "unit": "jar",
        "attributes": ["instant", "100% pure coffee", "bold"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=200&auto=format&fit=crop&q=80",
        "description": "Rich and bold signature coffee aroma with unforgettable taste."
    },
    {
        "name": "Coca-Cola Original 750ml",
        "hindi_name": "कोका कोला",
        "brand": "Coca-Cola",
        "category": "Beverages",
        "price": 45.0,
        "unit": "bottle",
        "attributes": ["fizzy", "refreshing", "cola"],
        "availability": False,  # Out of stock for substitute demo
        "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=200&auto=format&fit=crop&q=80",
        "description": "Refreshing original crisp sparkling beverage."
    },
    {
        "name": "Pepsi Regular 750ml",
        "hindi_name": "पेप्सी",
        "brand": "Pepsi",
        "category": "Beverages",
        "price": 42.0,
        "unit": "bottle",
        "attributes": ["fizzy", "refreshing", "cola"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=200&auto=format&fit=crop&q=80",
        "description": "Bold, bubbly and delightfully sweet cola refreshment."
    },
    {
        "name": "Thums Up Strong Taste 750ml",
        "hindi_name": "थम्स अप",
        "brand": "Coca-Cola",
        "category": "Beverages",
        "price": 45.0,
        "unit": "bottle",
        "attributes": ["fizzy", "strong", "spiced cola"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=200&auto=format&fit=crop&q=80",
        "description": "Taste the thunder with intense charged spicy cola punch."
    },
    {
        "name": "Real Fruit Power Mixed Fruit Juice 1L",
        "hindi_name": "रियल मिक्स्ड फ्रूट जूस",
        "brand": "Real",
        "category": "Beverages",
        "price": 125.0,
        "unit": "tetra-pack",
        "attributes": ["fruit-juice", "vitamin-c", "no-preservatives"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=200&auto=format&fit=crop&q=80",
        "description": "Delicious 9-fruit blend packed with natural vitality and Vitamin C."
    },

    # Snacks
    {
        "name": "Lay's India's Magic Masala Chips 50g",
        "hindi_name": "लेज मैजिक मसाला चिप्स",
        "brand": "Lay's",
        "category": "Snacks",
        "price": 20.0,
        "unit": "packet",
        "attributes": ["masala", "crispy", "snack"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=200&auto=format&fit=crop&q=80",
        "description": "Crunchy ridge-cut potato chips smothered in spicy Indian herbs."
    },
    {
        "name": "Parle-G Original Gluco Biscuits 250g",
        "hindi_name": "पारले जी बिस्कुट",
        "brand": "Parle",
        "category": "Snacks",
        "price": 30.0,
        "unit": "packet",
        "attributes": ["glucose", "tea-time", "sweet"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=200&auto=format&fit=crop&q=80",
        "description": "Timeless glucose biscuit pairing seamlessly with morning chai."
    },
    {
        "name": "Britannia Good Day Cashew Cookies 200g",
        "hindi_name": "गुड डे काजू कुकीज",
        "brand": "Britannia",
        "category": "Snacks",
        "price": 45.0,
        "unit": "packet",
        "attributes": ["cashew", "butter cookies", "rich"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=200&auto=format&fit=crop&q=80",
        "description": "Rich butter cookies abundantly sprinkled with real cashew nuggets."
    },
    {
        "name": "Haldiram's Nagpur Aloo Bhujia 200g",
        "hindi_name": "हल्दीराम आलू भुजिया",
        "brand": "Haldiram's",
        "category": "Snacks",
        "price": 55.0,
        "unit": "packet",
        "attributes": ["namkeen", "spicy", "crunchy"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200&auto=format&fit=crop&q=80",
        "description": "Crispy fried strands of potato and moth flour spiced to perfection."
    },
    {
        "name": "Cadbury Dairy Milk Silk Chocolate 60g",
        "hindi_name": "कैडबरी डेयरी मिल्क सिल्क",
        "brand": "Cadbury",
        "category": "Snacks",
        "price": 85.0,
        "unit": "bar",
        "attributes": ["chocolate", "smooth", "sweet"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=200&auto=format&fit=crop&q=80",
        "description": "Silky smooth velvety milk chocolate bar."
    },

    # Meat & Eggs
    {
        "name": "Eggoz Farm Fresh White Eggs (Pack of 6)",
        "hindi_name": "अंडे",
        "brand": "Eggoz",
        "category": "Meat",
        "price": 58.0,
        "unit": "box",
        "attributes": ["farm-fresh", "protein-rich", "graded"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=200&auto=format&fit=crop&q=80",
        "description": "Nutrient dense farm-fresh brown and white table eggs."
    },
    {
        "name": "Fresh Antibiotic-Free Chicken Breast 500g",
        "hindi_name": "ताजा चिकन",
        "brand": "FreshFarm",
        "category": "Meat",
        "price": 190.0,
        "unit": "pack",
        "attributes": ["antibiotic-free", "tender", "lean"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=200&auto=format&fit=crop&q=80",
        "description": "Freshly cut skinless boneless chicken breast fillets."
    },

    # Personal Care
    {
        "name": "Colgate Strong Teeth Dental Cream 200g",
        "hindi_name": "कोलगेट टूथपेस्ट",
        "brand": "Colgate",
        "category": "Personal Care",
        "price": 115.0,
        "unit": "tube",
        "attributes": ["cavity-protection", "amino-shakti", "fresh"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1559591937-e1032d2077e6?w=200&auto=format&fit=crop&q=80",
        "description": "Strengthens teeth and provides all-around cavity defense."
    },
    {
        "name": "Sensodyne Rapid Relief Toothpaste 80g",
        "hindi_name": "सेंसोडाइन टूथपेस्ट",
        "brand": "Sensodyne",
        "category": "Personal Care",
        "price": 195.0,
        "unit": "tube",
        "attributes": ["sensitivity-relief", "fast-acting"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1559591937-e1032d2077e6?w=200&auto=format&fit=crop&q=80",
        "description": "Clinically proven rapid relief for tooth sensitivity."
    },
    {
        "name": "Dettol Original Germ Protection Soap 125g (Pack of 3)",
        "hindi_name": "डेटॉल साबुन",
        "brand": "Dettol",
        "category": "Personal Care",
        "price": 135.0,
        "unit": "pack",
        "attributes": ["antibacterial", "hygiene", "fragrant"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1607006314187-55dfd2d140e6?w=200&auto=format&fit=crop&q=80",
        "description": "Proven 99.9% germ protection bar soap with classic pine fragrance."
    },
    {
        "name": "Dove Daily Shine Shampoo 340ml",
        "hindi_name": "डव शैम्पू",
        "brand": "Dove",
        "category": "Personal Care",
        "price": 280.0,
        "unit": "bottle",
        "attributes": ["nutritive-serum", "smooth-hair"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=200&auto=format&fit=crop&q=80",
        "description": "Infused with Nutritive Serum for smooth, shiny hair every day."
    },

    # Household
    {
        "name": "Surf Excel Quick Wash Detergent Powder 1kg",
        "hindi_name": "सर्फ एक्सेल डिटर्जेंट",
        "brand": "Surf Excel",
        "category": "Household",
        "price": 150.0,
        "unit": "packet",
        "attributes": ["stain-removal", "fabric-care"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=200&auto=format&fit=crop&q=80",
        "description": "Superior formulation removing tough stains like mud and grease in 1 wash."
    },
    {
        "name": "Vim Dishwash Gel Lemon 500ml",
        "hindi_name": "विम डिशवॉश जेल",
        "brand": "Vim",
        "category": "Household",
        "price": 110.0,
        "unit": "bottle",
        "attributes": ["degreasing", "lemon-fragrance"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1585837575652-267c041d77d4?w=200&auto=format&fit=crop&q=80",
        "description": "Concentrated dish gel powered with lemon extracts for sparkling vessels."
    },
    {
        "name": "Lizol Disinfectant Floor Cleaner Citrus 1L",
        "hindi_name": "लिजोल फ्लोर क्लीनर",
        "brand": "Lizol",
        "category": "Household",
        "price": 195.0,
        "unit": "bottle",
        "attributes": ["disinfectant", "citrus", "99.9-germs"],
        "availability": True,
        "image_url": "https://images.unsplash.com/photo-1584813470613-5b1c1cad3d69?w=200&auto=format&fit=crop&q=80",
        "description": "Kills 99.9% germs while leaving a long-lasting pleasant citrus aroma."
    }
]

SUBSTITUTE_RULES = {
    "Regular Cow Milk 1L": [
        {
            "substitute_name": "Raw Pressery Almond Milk Unsweetened",
            "substitute_brand": "Raw Pressery",
            "category": "Dairy",
            "substitute_price": 180.0,
            "original_price": 65.0,
            "reason": "Popular lactose-free plant-based alternative with smooth creamy texture.",
            "attributes": ["plant-based", "lactose-free", "vegan"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1568651313337-b4d45544d6db?w=200&auto=format&fit=crop&q=80"
        },
        {
            "substitute_name": "Sofit Soy Milk Chocolate Flavored",
            "substitute_brand": "Sofit",
            "category": "Dairy",
            "substitute_price": 140.0,
            "original_price": 65.0,
            "reason": "High-protein dairy-free beverage option.",
            "attributes": ["plant-based", "protein-rich"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1588710929895-5cb95e68340e?w=200&auto=format&fit=crop&q=80"
        },
        {
            "substitute_name": "Oatly Oat Milk Barista Edition",
            "substitute_brand": "Oatly",
            "category": "Dairy",
            "substitute_price": 220.0,
            "original_price": 65.0,
            "reason": "Premium oat blend that foams perfectly for hot beverages.",
            "attributes": ["plant-based", "vegan"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?w=200&auto=format&fit=crop&q=80"
        }
    ],
    "Classic White Bread": [
        {
            "substitute_name": "Britannia 100% Whole Wheat Bread",
            "substitute_brand": "Britannia",
            "category": "Bakery",
            "substitute_price": 55.0,
            "original_price": 40.0,
            "reason": "High-fiber whole wheat flour alternative for healthier sandwiches.",
            "attributes": ["whole wheat", "atta", "fiber-rich"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=200&auto=format&fit=crop&q=80"
        },
        {
            "substitute_name": "The English Bakery Multigrain Bread",
            "substitute_brand": "The English Bakery",
            "category": "Bakery",
            "substitute_price": 65.0,
            "original_price": 40.0,
            "reason": "Wholesome seeded multi-grain loaf with nutty aroma.",
            "attributes": ["multigrain", "seeds"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=200&auto=format&fit=crop&q=80"
        }
    ],
    "Coca-Cola Original 750ml": [
        {
            "substitute_name": "Pepsi Regular 750ml",
            "substitute_brand": "Pepsi",
            "category": "Beverages",
            "substitute_price": 42.0,
            "original_price": 45.0,
            "reason": "Direct cola alternative with refreshing crisp taste and slightly sweeter finish.",
            "attributes": ["fizzy", "refreshing", "cola"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=200&auto=format&fit=crop&q=80"
        },
        {
            "substitute_name": "Thums Up Strong Taste 750ml",
            "substitute_brand": "Coca-Cola",
            "category": "Beverages",
            "substitute_price": 45.0,
            "original_price": 45.0,
            "reason": "Stronger spiced carbonated cola for an intense bubbly kick.",
            "attributes": ["fizzy", "strong"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=200&auto=format&fit=crop&q=80"
        }
    ],
    "Organic Strawberries": [
        {
            "substitute_name": "Organic Royal Gala Apples",
            "substitute_brand": "Organic India",
            "category": "Produce",
            "substitute_price": 260.0,
            "original_price": 280.0,
            "reason": "Fresh certified organic fruit option currently available in produce.",
            "attributes": ["organic", "fresh"],
            "availability": True,
            "image_url": "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?w=200&auto=format&fit=crop&q=80"
        }
    ]
}

SEASONAL_CATALOG = {
    "Summer": [
        {"name": "Alphonso Mangoes", "category": "Produce", "price": 450.0, "unit": "dozen", "reason": "Peak summer harvest, richly sweet and aromatic.", "image": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=200&auto=format&fit=crop&q=80"},
        {"name": "Fresh Watermelon", "category": "Produce", "price": 75.0, "unit": "piece", "reason": "Hydrating and cooling fruit for hot sunny afternoons.", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=200&auto=format&fit=crop&q=80"},
        {"name": "Tender Coconut Water", "category": "Beverages", "price": 60.0, "unit": "piece", "reason": "Natural electrolyte recharge for sunny days.", "image": "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?w=200&auto=format&fit=crop&q=80"},
        {"name": "Fresh Lemons", "category": "Produce", "price": 40.0, "unit": "pack", "reason": "Perfect for refreshing homemade lemonade/shikanji.", "image": "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=200&auto=format&fit=crop&q=80"},
        {"name": "Rooh Afza Herbal Syrup", "category": "Beverages", "price": 170.0, "unit": "bottle", "reason": "Classic cooling rose herbal sherbet concentrate.", "image": "https://images.unsplash.com/photo-1546173159-315724a31d9b?w=200&auto=format&fit=crop&q=80"}
    ],
    "Monsoon": [
        {"name": "Fresh Sweet Corn", "category": "Produce", "price": 30.0, "unit": "piece", "reason": "Perfect for roasting or boiling on rainy evenings.", "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=200&auto=format&fit=crop&q=80"},
        {"name": "Fresh Ginger (Adrak)", "category": "Produce", "price": 40.0, "unit": "250g", "reason": "Essential for warming rainy day masala chai.", "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=200&auto=format&fit=crop&q=80"},
        {"name": "Chai Masala Spice Blend", "category": "Pantry", "price": 95.0, "unit": "box", "reason": "Aromatic cloves, cinnamon & cardamom for monsoon tea.", "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=200&auto=format&fit=crop&q=80"},
        {"name": "Besan Gram Flour", "category": "Pantry", "price": 60.0, "unit": "packet", "reason": "Ideal for preparing piping hot crispy pakoras.", "image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=200&auto=format&fit=crop&q=80"}
    ],
    "Winter": [
        {"name": "Nagpur Oranges", "category": "Produce", "price": 120.0, "unit": "kg", "reason": "Winter citrus loaded with immune-boosting Vitamin C.", "image": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=200&auto=format&fit=crop&q=80"},
        {"name": "Delhi Red Carrots (Gajar)", "category": "Produce", "price": 45.0, "unit": "kg", "reason": "Sweet winter carrots for salads, soups and Gajar Ka Halwa.", "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5c317?w=200&auto=format&fit=crop&q=80"},
        {"name": "Fresh Green Peas (Matar)", "category": "Produce", "price": 50.0, "unit": "kg", "reason": "Tender and sweet podded green peas.", "image": "https://images.unsplash.com/photo-1592394533824-9440e5d68530?w=200&auto=format&fit=crop&q=80"},
        {"name": "Organic Jaggery (Gud)", "category": "Pantry", "price": 80.0, "unit": "packet", "reason": "Traditional warming winter natural sweetener.", "image": "https://images.unsplash.com/photo-1622484216278-831e5bb8266c?w=200&auto=format&fit=crop&q=80"}
    ]
}
