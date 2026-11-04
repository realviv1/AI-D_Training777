import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def count_tokens(text):
    return len(encoder.encode(text))


def chunk_text(text, chunk_size=120, overlap=20):
    tokens = encoder.encode(text)

    chunks = []

    start = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk = encoder.decode(tokens[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks