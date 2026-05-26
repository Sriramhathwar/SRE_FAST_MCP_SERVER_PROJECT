import sys

from llama_cpp import Llama

llm = None
def get_llm():

    global llm

    if llm is None:

        from llama_cpp import Llama

        llm = Llama(
    model_path="/Users/sriramkl/Documents/SRE_MCP_AI/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    verbose=False
)

    return llm

def ask_llm(prompt, max_tokens=200):
    get_llm()
    print("Inside ask_llm block", file=sys.stderr, flush=True)
    out = llm(prompt, max_tokens=max_tokens, temperature=0.2)
    return out["choices"][0]["text"].strip()