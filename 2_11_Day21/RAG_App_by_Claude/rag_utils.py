"""Reusable helpers for every task: reading, tokenizing, chunking,
embedding, ChromaDB storage/search and the AI call."""
from functools import lru_cache

import chromadb
import tiktoken

import config


# ---------- Task 1: read & tokenize ----------
def load_documents():
    """Return {filename: text} for every .txt file in the Documents folder."""
    docs = {}
    for path in sorted(config.DOCS_DIR.glob("*.txt")):
        docs[path.name] = path.read_text(encoding="utf-8")
    if not docs:
        raise FileNotFoundError(f"No .txt files found in {config.DOCS_DIR}")
    return docs


@lru_cache(maxsize=1)
def get_encoder():
    return tiktoken.get_encoding(config.TOKEN_ENCODING)


def count_tokens(text):
    return len(get_encoder().encode(text))


# ---------- Task 2: chunk & embed ----------
def chunk_text(text, size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP):
    """Split text into token windows of `size`, each overlapping the previous by `overlap`."""
    enc = get_encoder()
    tokens = enc.encode(text)
    step = size - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        window = tokens[start:start + size]
        chunks.append(enc.decode(window).strip())
        if start + size >= len(tokens):
            break
    return chunks


def chunk_documents(docs):
    """Return a list of dicts: {id, text, source, chunk_index, token_count}."""
    all_chunks = []
    for filename, text in docs.items():
        for i, chunk in enumerate(chunk_text(text)):
            all_chunks.append({
                "id": f"{filename}::chunk{i}",
                "text": chunk,
                "source": filename,
                "chunk_index": i,
                "token_count": count_tokens(chunk),
            })
    return all_chunks


@lru_cache(maxsize=1)
def get_embedder():
    # Imported here so Task 1 runs fast without loading PyTorch.
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(config.EMBED_MODEL)


def embed(texts):
    """Return a list of embedding vectors (lists of floats)."""
    vectors = get_embedder().encode(texts, normalize_embeddings=True)
    return vectors.tolist()


# ---------- Task 3: ChromaDB ----------
def get_collection():
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return client.get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},   # distances returned are cosine distances
    )


def build_collection():
    """(Re)index every chunk with its embedding and source filename. Returns the collection."""
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        client.delete_collection(config.COLLECTION_NAME)   # start clean on each rebuild
    except Exception:
        pass
    collection = client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    chunks = chunk_documents(load_documents())
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embed([c["text"] for c in chunks]),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    return collection


def ensure_collection():
    """Use the saved DB if it already has data, otherwise build it."""
    collection = get_collection()
    if collection.count() == 0:
        collection = build_collection()
    return collection


def search(question, k=config.TOP_K):
    """Return the top-k chunks as dicts: {text, source, distance}."""
    collection = ensure_collection()
    result = collection.query(
        query_embeddings=embed([question]),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for text, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append({"text": text, "source": meta["source"], "distance": dist})
    return hits


# ---------- Task 4: AI answer ----------
NOT_FOUND = "I cannot find the answer in the provided documents."

SYSTEM_PROMPT = (
    "You are a company policy assistant. Answer the question using ONLY the "
    "context provided. Do not use outside knowledge or make assumptions. "
    f"If the context does not contain the answer, reply exactly: \"{NOT_FOUND}\" "
    "Keep answers short and mention the source file name."
)


def build_prompt(question, hits):
    context = "\n\n".join(
        f"[Source: {h['source']}]\n{h['text']}" for h in hits
    )
    return f"Context:\n{context}\n\nQuestion: {question}"


def ask_ai(question, hits):
    prompt = build_prompt(question, hits)

    if config.AI_PROVIDER == "anthropic":
        import anthropic
        client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY
        response = client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    if config.AI_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI()                       # reads OPENAI_API_KEY
        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()

    raise ValueError(f"Unknown AI_PROVIDER '{config.AI_PROVIDER}'. Use 'anthropic' or 'openai'.")
