from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

files = [
    "Documents/Visitor_Guide.txt",
    "Documents/Workshops_and_Events.txt"
]

docs = []

for file in files:
    loader = TextLoader(file)
    docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)

chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="museum_langchain"
)

question = input("Enter question: ")

results = db.similarity_search_with_score(question, k=2)

for doc, score in results:
    print("\nSOURCE:", doc.metadata["source"])
    print("DISTANCE:", score)
    print(doc.page_content)