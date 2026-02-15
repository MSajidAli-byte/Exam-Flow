import chromadb
import os

# Connect to the persistent database
# Inside Docker, this path is /app/chroma_db
DB_PATH = os.path.join(os.getcwd(), "chroma_db") 

print(f"📂 Connecting to ChromaDB at: {DB_PATH}")

try:
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # List all collections
    collections = client.list_collections()
    print(f"📚 Found {len(collections)} collections.")
    
    for col in collections:
        count = col.count()
        print(f"   - Collection '{col.name}': {count} documents")
        
        # Peek at the data
        if count > 0:
            peek = col.peek(limit=1)
            print(f"     👀 Sample ID: {peek['ids'][0]}")
            print(f"     👀 Sample Metadata: {peek['metadatas'][0]}")

except Exception as e:
    print(f"❌ Error connecting to ChromaDB: {e}")
