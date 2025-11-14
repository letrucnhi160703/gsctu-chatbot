import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

db = FAISS.load_local(
    "dataset/faiss_index",
    OllamaEmbeddings(model="nomic-embed-text"),
    allow_dangerous_deserialization=True
)

docs = db.similarity_search("Luận án tiến sĩ được trình bày ở đâu?", k=3)

for i, doc in enumerate(docs, 1):
    print(f"\n--- Kết quả {i} ---")
    print(doc.page_content)