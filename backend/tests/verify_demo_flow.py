import sys
import httpx

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api"

def run_demo_flow_tests():
    print("=================================================================")
    print("  RUNNING VOCACART AI DEMO INTEGRATION SCENARIO VERIFICATION")
    print("=================================================================")

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # Reset list
        client.post("/shopping-list/clear")

        # Step 1: Multi-item Add
        print("\n--- [Step 1] Multi-Item Voice Command ---")
        prompt1 = "I need two packets of milk, five apples and a loaf of bread"
        print(f"User speech: \"{prompt1}\"")
        r1 = client.post("/command", json={"text": prompt1})
        assert r1.status_code == 200, r1.text
        data1 = r1.json()
        print(f"-> Intent: {data1['intent']}")
        print(f"-> Items detected: {len(data1['entities']['items'])}")
        print(f"-> Confirmation: {data1['message']}")
        print(f"-> TTS Text: {data1['tts_message']}")
        assert data1['intent'] == "ADD_ITEMS"
        assert len(data1['entities']['items']) == 3

        # Verify List
        r_list = client.get("/shopping-list")
        items = r_list.json()
        names = [i["name"] for i in items]
        print(f"-> Current Shopping List: {names}")
        assert any("Milk" in n for n in names)
        assert any("Apple" in n for n in names)
        assert any("Bread" in n for n in names)

        # Step 2: Remove Item
        print("\n--- [Step 2] Remove Item Voice Command ---")
        prompt2 = "Remove bread"
        print(f"User speech: \"{prompt2}\"")
        r2 = client.post("/command", json={"text": prompt2})
        assert r2.status_code == 200
        data2 = r2.json()
        print(f"-> Confirmation: {data2['message']}")
        assert data2['intent'] == "REMOVE_ITEM"

        # Verify List without Bread
        r_list2 = client.get("/shopping-list")
        names2 = [i["name"] for i in r_list2.json()]
        print(f"-> Shopping List after removal: {names2}")
        assert not any("Bread" in n for n in names2)

        # Step 3: Product Search with Price Bounds
        print("\n--- [Step 3] Voice Product Search with Filters ---")
        prompt3 = "Find organic apples under 300 rupees"
        print(f"User speech: \"{prompt3}\"")
        r3 = client.post("/command", json={"text": prompt3})
        assert r3.status_code == 200
        data3 = r3.json()
        print(f"-> Intent: {data3['intent']}")
        print(f"-> Search Query: {data3['entities']['query']}, Max Price: {data3['entities']['max_price']}")
        print(f"-> Results Found: {len(data3['search_results'])}")
        for prod in data3['search_results']:
            print(f"   * {prod['name']} - ₹{prod['price']} ({prod['category']}) [{', '.join(prod['attributes'])}]")
        assert data3['intent'] == "SEARCH_PRODUCT"
        assert len(data3['search_results']) >= 1

        # Step 4: Smart Recommendations
        print("\n--- [Step 4] Smart Restock Recommendations ---")
        prompt4 = "What should I buy?"
        print(f"User speech: \"{prompt4}\"")
        r4 = client.get("/recommendations")
        assert r4.status_code == 200
        recs = r4.json()
        print(f"-> Recommendations Generated: {len(recs)}")
        for rec in recs[:3]:
            print(f"   * [{rec['category']}] {rec['product_name']} (Score: {int(rec['score']*100)}%)")
            print(f"     Reason: {rec['reason']}")
            print(f"     💡 Explainable Rationale: {rec['explanation']}")

        # Step 5: In-Store Shopping Mode - Mark Purchased
        print("\n--- [Step 5] Shopping Mode Voice Mark Purchased ---")
        prompt5 = "I've bought the milk"
        print(f"User speech: \"{prompt5}\"")
        r5 = client.post("/command", json={"text": prompt5})
        assert r5.status_code == 200
        data5 = r5.json()
        print(f"-> Intent: {data5['intent']}")
        print(f"-> Confirmation: {data5['message']}")
        print(f"-> Next Item Audio: \"{data5['tts_message']}\"")
        assert data5['intent'] == "MARK_PURCHASED"

        # Step 6: Multilingual Hinglish & Devanagari Hindi
        print("\n--- [Step 6] Multilingual Support (Hinglish & Hindi) ---")
        prompt_hinglish = "Do packet Amul milk aur 5 apples add karo"
        print(f"Hinglish: \"{prompt_hinglish}\"")
        rh = client.post("/command", json={"text": prompt_hinglish, "language_hint": "hinglish"})
        assert rh.status_code == 200
        print(f"-> Hinglish Intent: {rh.json()['intent']}, Message: {rh.json()['message']}")

        prompt_hindi = "मुझे दो किलो चावल चाहिए"
        print(f"Hindi: \"{prompt_hindi}\"")
        r_hi = client.post("/command", json={"text": prompt_hindi, "language_hint": "hi"})
        assert r_hi.status_code == 200
        print(f"-> Hindi Intent: {r_hi.json()['intent']}, Message: {r_hi.json()['message']}")

        # Step 7: Substitutes for Unavailable Items
        print("\n--- [Step 7] Substitute Engine for Unavailable Items ---")
        r_sub = client.get("/substitutes/Regular Cow Milk 1L")
        assert r_sub.status_code == 200
        subs = r_sub.json()
        print(f"-> Substitutes for Out-of-Stock Regular Cow Milk: {len(subs)}")
        for s in subs:
            print(f"   * 🥛 {s['substitute_name']} - ₹{s['substitute_price']}")
            print(f"     💡 Rationale: {s['reason']}")

        # Step 8: AI Insights
        print("\n--- [Step 8] AI Insights Summary ---")
        r_ins = client.get("/insights")
        assert r_ins.status_code == 200
        ins = r_ins.json()
        print(f"-> Total Estimated List Budget: ₹{ins['total_estimated_budget']}")
        print(f"-> Shopping Pattern Insight: {ins['weekly_shopping_habit']}")

        print("\n=================================================================")
        print("  ✓ ALL 8 DEMO SCENARIO STAGES PASSED WITH 100% SUCCESS!")
        print("=================================================================")

if __name__ == "__main__":
    run_demo_flow_tests()
