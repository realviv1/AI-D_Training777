"""Task 4 - Retrieve chunks and ask the AI to answer only from that context.

Usage:
    python task4_ai_answer.py                      # runs all 5 test questions
    python task4_ai_answer.py "Your question here"
"""
import sys

import config
from rag_utils import search, ask_ai


def answer(question):
    hits = search(question)
    print("=" * 70)
    print(f"QUESTION: {question}")
    print("Retrieved:")
    for h in hits:
        print(f"  - {h['source']} (cosine distance {h['distance']:.4f})")
    print(f"\nAI ANSWER ({config.AI_PROVIDER}):")
    print(ask_ai(question, hits))
    print()


def main():
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else config.TEST_QUESTIONS
    for q in questions:
        answer(q)


if __name__ == "__main__":
    main()
