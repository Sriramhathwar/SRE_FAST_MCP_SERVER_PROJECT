import faiss
import numpy as np
import sys

embedding_model = None

def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        from sentence_transformers import SentenceTransformer

        print("Loading embeddings...", file=sys.stderr, flush=True)

        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return embedding_model



def retrieve_docs(query):
    model = get_embedding_model()

    texts = open("/Users/sriramkl/Documents/SRE_Fastmcp_Server_AI_Project/rag/data/runbooks.txt").read().split("\n\n")
    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k=2)

    return "\n\n".join([texts[i] for i in I[0]])


