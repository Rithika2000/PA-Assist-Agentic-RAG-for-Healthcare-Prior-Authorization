# embed.py
# This file converts all text chunks into numbers
# and stores them in ChromaDB database

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import (
    load_payer_policies,
    load_guidelines,
    load_procedure_codes,
    load_patient_notes
)

# ----------------------------------------
# SETUP
# ----------------------------------------

# This model converts text into numbers
# It's free and runs locally on your Mac
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded!")

# This creates your local database
# All data saved in data/chromadb folder
client = chromadb.PersistentClient(path="data/chromadb")


# ----------------------------------------
# FUNCTION: Embed and Store in ChromaDB
# ----------------------------------------
def embed_and_store(chunks, collection_name):
    """
    Takes a list of text chunks
    Converts each to numbers (embeddings)
    Stores in ChromaDB collection
    """

    # Get or create a collection (like a table in database)
    col = client.get_or_create_collection(collection_name)

    # Extract just the text from each chunk
    texts = []
    metadatas = []

    for chunk in chunks:
        # Handle both LangChain Document objects and plain dicts
        if hasattr(chunk, 'page_content'):
            texts.append(chunk.page_content)
            metadatas.append(chunk.metadata)
        else:
            texts.append(chunk["text"])
            metadatas.append({
                "source_type": chunk.get("source_type", "unknown"),
                "filename": chunk.get("filename", "unknown")
            })

    if not texts:
        print(f"❌ No texts to embed for {collection_name}")
        return

    print(f"   Converting {len(texts)} chunks to numbers...")

    # Convert all texts to numbers at once
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32
    )

    print(f"   Storing in ChromaDB...")

    # Store everything in ChromaDB
    for i, (text, meta, emb) in enumerate(
        zip(texts, metadatas, embeddings)
    ):
        col.add(
            ids=[f"{collection_name}_{i}"],
            embeddings=[emb.tolist()],
            documents=[text],
            metadatas=[meta]
        )

    print(f"✅ Stored {len(texts)} chunks in '{collection_name}'")


# ----------------------------------------
# MAIN: Run Everything
# ----------------------------------------
if __name__ == "__main__":
    print("\n🚀 Starting embedding process...\n")

    # Step 1: Load all data
    print("📋 Loading Payer Policies...")
    policies = load_payer_policies()

    print("\n📚 Loading Clinical Guidelines...")
    guidelines = load_guidelines()

    print("\n💊 Loading Procedure Codes...")
    codes = load_procedure_codes()

    print("\n👤 Loading Patient Notes...")
    patients = load_patient_notes()

    # Step 2: Embed and store each dataset
    print("\n" + "="*50)
    print("💾 EMBEDDING AND STORING IN CHROMADB")
    print("="*50 + "\n")

    print("📋 Embedding Payer Policies...")
    embed_and_store(policies, "payer_policies")

    print("\n📚 Embedding Clinical Guidelines...")
    embed_and_store(guidelines, "clinical_guidelines")

    print("\n💊 Embedding Procedure Codes...")
    embed_and_store(codes, "procedure_codes")

    print("\n👤 Embedding Patient Notes...")
    embed_and_store(patients, "patient_notes")

    # Step 3: Verify everything stored correctly
    print("\n" + "="*50)
    print("✅ VERIFICATION - Checking ChromaDB")
    print("="*50)

    collections = [
        "payer_policies",
        "clinical_guidelines",
        "procedure_codes",
        "patient_notes"
    ]

    total = 0
    for name in collections:
        col = client.get_collection(name)
        count = col.count()
        total += count
        print(f"   {name}: {count} chunks stored")

    print(f"\n🎉 Total chunks in ChromaDB: {total}")
    print("\n✅ embed.py complete!")
    print("   Your knowledge base is ready!")
    print("   Next step: agent.py")