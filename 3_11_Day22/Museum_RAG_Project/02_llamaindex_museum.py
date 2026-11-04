from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, Settings

documents = SimpleDirectoryReader("Documents").load_data()

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

splitter = SentenceSplitter(
    chunk_size=150,
    chunk_overlap=20
)

nodes = splitter.get_nodes_from_documents(documents)

index = VectorStoreIndex(nodes)

retriever = index.as_retriever(similarity_top_k=2)

question = input("Enter question: ")

results = retriever.retrieve(question)

for node in results:
    print("\nSOURCE:", node.metadata.get("file_name"))
    print("SCORE:", node.score)
    print(node.text)