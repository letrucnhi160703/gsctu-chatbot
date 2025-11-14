import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

DATA_PATH = "dataset/processed_data.txt"
VECTOR_PATH = "dataset/faiss_index"
BATCH_SIZE = 200


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_into_chunks(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def build_embeddings(chunks, batch_size=BATCH_SIZE):
    embed_model = OllamaEmbeddings(model="bge-m3")
    vector_store = None

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        print(f"Embedding batch {i} → {i+len(batch)} ...")

        if vector_store is None:
            vector_store = FAISS.from_texts(batch, embed_model)
        else:
            vector_store.add_texts(batch)

    return vector_store


def save_vectorstore(store, path):
    os.makedirs(path, exist_ok=True)
    store.save_local(path)
    print(f"Saved vector DB to: {path}")


def main():
    print("Loading text...")
    text = load_text(DATA_PATH)

    print("Splitting into chunks...")
    chunks = split_into_chunks(text)

    print(f"Total chunks: {len(chunks)}")

    print("Generating embeddings...")
    store = build_embeddings(chunks)

    print("Saving vector store...")
    save_vectorstore(store, VECTOR_PATH)

    print("Done!")


if __name__ == "__main__":
    main()
