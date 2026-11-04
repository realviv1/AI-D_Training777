from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

with open("Documents/Visitor_Guide.txt", "r", encoding="utf-8") as f:
    visitor_text = f.read()

with open("Documents/Workshops_and_Events.txt", "r", encoding="utf-8") as f:
    workshop_text = f.read()

documents = [
    Document(content=visitor_text, meta={"source": "Visitor_Guide.txt"}),
    Document(content=workshop_text, meta={"source": "Workshops_and_Events.txt"})
]

splitter = DocumentSplitter(
    split_by="word",
    split_length=100,
    split_overlap=15
)

chunks = splitter.run(documents=documents)["documents"]

document_store = InMemoryDocumentStore()

doc_embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

doc_embedder.warm_up()

embedded_docs = doc_embedder.run(chunks)["documents"]

document_store.write_documents(embedded_docs)

text_embedder = SentenceTransformersTextEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

text_embedder.warm_up()

question = input("Enter question: ")

query_embedding = text_embedder.run(question)["embedding"]

retriever = InMemoryEmbeddingRetriever(
    document_store=document_store,
    top_k=2
)

results = retriever.run(query_embedding=query_embedding)

for doc in results["documents"]:
    print("\nSOURCE:", doc.meta["source"])
    print(doc.content)