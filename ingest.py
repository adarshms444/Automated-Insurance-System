import os
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv # Import dotenv
import time

# --- CONFIGURATION ---
load_dotenv() # Load variables from .env

# GET KEYS FROM ENVIRONMENT
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Validation
if not GEMINI_API_KEY or not PINECONE_API_KEY:
    print("❌ Error: Keys not found in .env file.")
    exit()

# Configure APIs
genai.configure(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

def create_index_if_missing():
    """Creates the Pinecone Index if it doesn't exist."""
    existing_indexes = [index.name for index in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"⚙️ Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=768, # Matches Gemini text-embedding-004
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        time.sleep(10) # Wait for initialization
    else:
        print(f"✅ Index '{INDEX_NAME}' already exists.")

def load_and_chunk_md_files():
    """Reads .md files from data/ and prepares them for upload."""
    documents = []
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        print("❌ Error: 'data' folder not found!")
        return []

    print("📂 Reading files from 'data/' folder...")
    for filename in os.listdir(data_folder):
        if filename.endswith(".md"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Use filename as ID and Title
                doc_id = filename.replace(".md", "")
                category = doc_id.replace("_", " ").title()
                
                documents.append({
                    "id": doc_id,
                    "text": content,
                    "category": category
                })
                print(f"   -> Found: {filename}")
    return documents

def upload_to_pinecone(documents):
    """Generates embeddings and uploads to Pinecone."""
    index = pc.Index(INDEX_NAME)
    print("\n🚀 Starting Upload Process...")
    
    for doc in documents:
        print(f"   Processing: {doc['id']}...")
        try:
            # 1. Generate Embedding
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=doc['text'],
                task_type="retrieval_document"
            )
            embedding = response['embedding']
            
            # 2. Upload to Pinecone
            index.upsert(vectors=[{
                "id": doc['id'],
                "values": embedding,
                "metadata": {
                    "text": doc['text'],
                    "category": doc['category']
                }
            }])
            print(f"   ✅ Uploaded!")
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")

if __name__ == "__main__":
    create_index_if_missing()
    docs = load_and_chunk_md_files()
    if docs:
        upload_to_pinecone(docs)
        print("\n🎉 Success! Knowledge Base is updated.")
    else:
        print("\n⚠️ No documents found. Check data folder.")
