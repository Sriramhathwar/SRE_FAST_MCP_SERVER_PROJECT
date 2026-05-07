from llama_cpp import Llama

llm = Llama(
    model_path="/Users/sriramkl/Documents/SRE_MCP_AI/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    verbose=False
)

def ask_llm(prompt, max_tokens=200):
    print("Inside ask_llm block")
    out = llm(prompt, max_tokens=max_tokens, temperature=0.2)
    return out["choices"][0]["text"].strip()