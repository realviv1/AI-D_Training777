"""Task 2 - Split into 120-token chunks with 20-token overlap, then embed."""
import config
from rag_utils import load_documents, chunk_documents, embed


def main():
    chunks = chunk_documents(load_documents())

    print(f"Chunk size: {config.CHUNK_SIZE} tokens | Overlap: {config.CHUNK_OVERLAP} tokens")
    print(f"Total chunks: {len(chunks)}")
    for source in sorted({c['source'] for c in chunks}):
        n = sum(1 for c in chunks if c["source"] == source)
        print(f"  - {source}: {n} chunks")

    print("\nAll chunks:")
    for c in chunks:
        print(f"  {c['id']:<45} {c['token_count']:>4} tokens")

    sample = chunks[0]
    print("\n" + "-" * 70)
    print(f"SAMPLE CHUNK: {sample['id']} ({sample['token_count']} tokens)")
    print("-" * 70)
    print(sample["text"])
    print("-" * 70)

    print(f"\nLoading embedding model '{config.EMBED_MODEL}' ...")
    vectors = embed([c["text"] for c in chunks])
    print(f"Embeddings generated: {len(vectors)}")
    print(f"Vector size (dimensions): {len(vectors[0])}")
    print(f"First 5 values of sample vector: {[round(v, 4) for v in vectors[0][:5]]}")


if __name__ == "__main__":
    main()
