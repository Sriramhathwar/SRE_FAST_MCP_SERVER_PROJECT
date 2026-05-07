from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = open("/Users/sriramkl/Documents/SRE_Fastmcp_Server_AI_Project/rag/data/runbooks.txt").read().split("\n\n")
embeddings = model.encode(texts)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings))

def retrieve_docs(query):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k=2)

    return "\n\n".join([texts[i] for i in I[0]])