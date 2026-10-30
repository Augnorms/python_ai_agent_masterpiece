import chromadb
from sentence_transformers import SentenceTransformer
import io
import docx
import pypdf
from database.database import save_document_chunks, get_swarm_settings

# Connect to Docker ChromaDB
chroma_client = chromadb.HttpClient(host='localhost', port=8001)

_model_cache = {}

def get_embedding_model(session_id: str = "default") -> SentenceTransformer:
    """Returns a cached SentenceTransformer instance according to active settings."""
    try:
        settings = get_swarm_settings(session_id)
        model_name = settings.get("embedding_model") or "all-MiniLM-L6-v2"
    except Exception as e:
        model_name = "all-MiniLM-L6-v2"

    if model_name not in _model_cache:
        print(f"[RAG] Loading embedding model into memory: {model_name}...")
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]

# Backwards compatibility reference
embedding_model = get_embedding_model("default")

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extracts text based on file format (.docx, .pdf, .txt, .md, etc.)."""
    lower_name = filename.lower()
    
    # 1. Handle DOCX files
    if lower_name.endswith('.docx'):
        doc = docx.Document(io.BytesIO(file_content))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        # Also include any table content
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
                if row_text:
                    paragraphs.append(row_text)
        return "\n\n".join(paragraphs)
        
    # 2. Handle PDF files
    elif lower_name.endswith('.pdf'):
        reader = pypdf.PdfReader(io.BytesIO(file_content))
        pages_text = [page.extract_text().strip() for page in reader.pages if page.extract_text()]
        return "\n\n".join(pages_text)
        
    # 3. Handle Plain Text, Markdown, JSON, etc.
    else:
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback for Windows-1252 / Latin-1 encoded text files
            return file_content.decode('latin-1', errors='ignore')


def process_and_ingest_file(file_content: bytes, filename: str):
    """Reads a file, chunks it, embeds it, and saves it to ChromaDB."""
    try:
        # 1. Extract plain text from the file (supporting binary docx, pdf, txt, etc.)
        text = extract_text_from_file(file_content, filename)
        
        if not text or not text.strip():
            return "File was empty or contained no extractable text."
        
        # 2. Chunk the text (split by paragraphs)
        # 2. Smart Chunking
        chunks = []
        
        # If it's markdown or text, split by headings or keep tables together
        if filename.lower().endswith(('.md', '.txt', '.pdf', '.docx', '.xlsx')):
            # Split by markdown headers (e.g., #, ##, ###)
            import re
            sections = re.split(r'\n(?=#)', text)
            
            for section in sections:
                if len(section) > 1000:
                    paragraphs = section.split("\n\n")
                    current_chunk = ""
                    for p in paragraphs:
                        if len(current_chunk) + len(p) < 1000:
                            current_chunk += p + "\n\n"
                        else:
                            if current_chunk.strip(): chunks.append(current_chunk.strip())
                            current_chunk = p + "\n\n"
                    if current_chunk.strip(): chunks.append(current_chunk.strip())
                else:
                    if section.strip():
                        chunks.append(section.strip())
        else:
            # Standard paragraph split for PDFs/DOCX
            chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

        # Fallback if no chunks
        if not chunks:
            chunks = [text.strip()]

        # Save chunks to Postgres for Hybrid (Keyword) Search
        save_document_chunks(filename, chunks)    

        # 3. Create embeddings using active model
        model = get_embedding_model()
        embeddings = model.encode(chunks).tolist()
        
        # 4. Save to ChromaDB
        collection = chroma_client.get_or_create_collection(name="company_docs")
        
        # Create safe unique IDs based on filename and chunk index
        safe_filename = filename.replace(" ", "_")
        ids = [f"{safe_filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in chunks]
        
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        
        return f"Successfully ingested {len(chunks)} chunks into ChromaDB."
        
    except Exception as e:
        raise Exception(f"Ingestion failed: {str(e)}")