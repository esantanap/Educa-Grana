# scripts/test_chroma_local.py
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings

persist_dir = str(Path("chroma").resolve())

docs = [Document(page_content="hello world", metadata={"source": "test"})]
emb = FakeEmbeddings(size=1536)

db = Chroma.from_documents(
    documents=docs,
    embedding=emb,
    persist_directory=persist_dir,
    collection_name="test_collection",
)
db.persist()
print("OK persist")
retriever = db.as_retriever()
print(retriever.invoke("hello"))
