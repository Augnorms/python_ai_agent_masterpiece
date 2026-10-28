import chromadb
from sentence_transformers import SentenceTransformer

#connect to chroma database using client
chroma_client = chromadb.HttpClient(host='localhost', port=8001)

#get or create a collection of table like sql
collection = chroma_client.get_or_create_collection(name="company_docs")

# 2. Load the local embedding model
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Read and Chunk the document
print("Reading document...")
with open("company_policy.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split by double newlines (paragraphs)
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print(f"Split document into {len(chunks)} chunks.")

print("creating embeddings...")
embeddings = model.encode(chunks).tolist()

# 5. Save to ChromaDB
ids = [f"chunk_{i}" for i in range(len(chunks))]
metadatas = [{"source": "company_policy.txt"} for _ in chunks]

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

print("Successfully ingested document into ChromaDB!")
