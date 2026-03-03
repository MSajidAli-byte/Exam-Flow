
import requests
import json

BACKEND_URL = "http://localhost:8000"

def list_cache():
    try:
        response = requests.get(f"{BACKEND_URL}/cache/list")
        if response.status_code == 200:
            items = response.json().get("items", [])
            print(f"Found {len(items)} items in cache:")
            for item in items:
                print(f"ID: {item['id']} | Filename: {item.get('filename', 'Unknown')} | Snippet: {item['preview'][:50]}...")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_cache()
