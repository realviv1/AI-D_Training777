"""Run all four tasks in order."""
import task1_read_tokenize
import task2_chunk_embed
import task3_store_search
import task4_ai_answer


def banner(title):
    print("\n" + "#" * 70)
    print(f"#  {title}")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    banner("TASK 1 - Read and tokenize")
    task1_read_tokenize.main()
    banner("TASK 2 - Chunk and embed")
    task2_chunk_embed.main()
    banner("TASK 3 - Store and search in ChromaDB")
    task3_store_search.main()
    banner("TASK 4 - AI answers")
    task4_ai_answer.main()
