"""Task 3 - Store every chunk in a persistent ChromaDB and search it.

Usage:
    python task3_store_search.py                      # uses the first test question
    python task3_store_search.py "Your question here"
"""
import sys

import config
from rag_utils import build_collection, search


def show_results(question, hits):
    print(f"\nQUESTION: {question}")
    print(f"Top {len(hits)} chunks (lower cosine distance = more similar):")
    for rank, h in enumerate(hits, start=1):
        print("-" * 70)
        print(f"#{rank} | Source: {h['source']} | Cosine distance: {h['distance']:.4f}")
        print(h["text"])
    print("-" * 70)


def main():
    print("Building persistent ChromaDB ...")
    collection = build_collection()
    print(f"Saved {collection.count()} chunks to: {config.CHROMA_DIR}")

    question = " ".join(sys.argv[1:]) or config.TEST_QUESTIONS[0]
    show_results(question, search(question))


if __name__ == "__main__":
    main()
