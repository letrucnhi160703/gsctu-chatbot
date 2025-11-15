from langchain_community.embeddings import OllamaEmbeddings

embed = OllamaEmbeddings(model="nomic-embed-text")
text = "Test embedding"
print(embed.embed_query(text))