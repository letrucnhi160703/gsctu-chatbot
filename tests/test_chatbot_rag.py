import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

VECTOR_PATH = "dataset/faiss_index"
EMBED_MODEL_NAME = "bge-m3"
LLM_MODEL_NAME = "llama3.2:3b"
TOP_K = 4
SHOW_SOURCES = True

print("Đang tải vector store...")
embed_model = OllamaEmbeddings(model=EMBED_MODEL_NAME)

db = FAISS.load_local(
    folder_path=VECTOR_PATH,
    embeddings=embed_model,
    allow_dangerous_deserialization=True,
)

retriever = db.as_retriever(search_kwargs={"k": TOP_K})
print("Tải vector store thành công.")

print(f"Khởi tạo LLM: {LLM_MODEL_NAME}")
llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0.1)

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        Bạn là trợ lý AI có khả năng trả lời chính xác dựa trên tài liệu.

        ===== NGỮ CẢNH =====
        {context}
        ===== HẾT NGỮ CẢNH =====

        Câu hỏi: {question}

        YÊU CẦU:
        - Chỉ dùng thông tin trong ngữ cảnh.
        - Nếu ngữ cảnh không chứa câu trả lời, hãy nói: "Trong dữ liệu hiện có không thấy thông tin về vấn đề này."
        - Trả lời ngắn gọn, tiếng Việt rõ ràng.

        Trả lời:
        """,
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=SHOW_SOURCES,
    chain_type_kwargs={"prompt": rag_prompt},
)


def chat():
    print("\n===== CHATBOT RAG TỐI ƯU =====\nNhập câu hỏi, 'exit' để thoát.\n")

    while True:
        query = input("Bạn: ").strip()
        if query.lower() in ["exit", "quit", "thoát"]:
            print("Tạm biệt!")
            break
        if not query:
            continue

        try:
            result = qa.invoke({"query": query})
            answer = result["result"].strip()
            print(f"\nBot: {answer}\n")

        except Exception as e:
            print(f"Lỗi: {e}")


if __name__ == "__main__":
    chat()
