import sys
import os
import requests

# We call a new backend endpoint to clear the cache via API
BACKEND_URL = "http://localhost:8000"

def show_list():
    try:
        resp = requests.get(f"{BACKEND_URL}/cache/list")
        if resp.status_code == 200:
            items = resp.json()
            if not items:
                print("📭 Cache is currently empty.")
                return None
            print("\n📋 CURRENT CACHED ANALYSES:")
            print("-" * 60)
            for i, item in enumerate(items):
                print(f"[{i}] ID: {item['id']}")
                print(f"    Type: {item['type']} | {item['preview']}\n")
            return items
    except Exception as e:
        print(f"❌ Error listing cache: {e}")
    return None

def reset():
    items = show_list()
    
    print("\n[Options]")
    print("ALL  - Clear everything")
    print("EXIT - Close script")
    if items:
        print("0,1,2... - Clear specific item by index")
    
    choice = input("\nSelect an option: ").strip().upper()
    
    if choice == "EXIT":
        return
    elif choice == "ALL":
        target_id = None
    elif choice.isdigit() and items and int(choice) < len(items):
        target_id = items[int(choice)]['id']
    else:
        print("Invalid choice.")
        return

    print(f"🧹 Requesting reset for: {target_id if target_id else 'EVERYTHING'}...")
    try:
        params = {"item_id": target_id} if target_id else {}
        response = requests.post(f"{BACKEND_URL}/cache/clear", params=params)
        if response.status_code == 200:
            print("✅ SUCCESS!")
        else:
            print(f"❌ FAILED: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    reset()
