import os

from chunking import (
    read_file,
    count_tokens,
    chunk_text
)

from vector_store import (
    add_chunks,
    search
)

from ai_answer import get_answer


folder = "Documents"

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    text = read_file(path)

    print("\n================================")
    print(file)

    token_count = count_tokens(text)

    print("Tokens:", token_count)

    chunks = chunk_text(text)

    print("Chunks:", len(chunks))

    print("\nSample Chunk:\n")
    print(chunks[0])

    add_chunks(chunks, file)

print("\nDocuments indexed.")

while True:

    question = input("\nAsk Question: ")

    results = search(question)

    docs = results["documents"][0]
    distances = results["distances"][0]

    print("\nTop 2 Chunks:")

    for i in range(len(docs)):
        print("\nChunk", i + 1)
        print(docs[i])
        print("Distance:", distances[i])

    context = "\n".join(docs)

    answer = get_answer(
        question,
        context
    )

    print("\nAI Answer:")
    print(answer)