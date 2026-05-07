import requests
from agent.llm import ask_llm

MCP_URL = "http://127.0.0.1:8000/mcp"

def decide_tools(query):
    print("Inside decide_tools block")
    prompt = f"""
You are a classifier.

Your job:
Select relevant tools for the query.

Available tools:
- metrics
- logs
- runbook

Rules:
- Return ONLY tool names
- No explanation
- No sentences
- No numbering
- Output must be comma-separated
- Example output: metrics,logs

Query: {query}

Output:
"""
    res = ask_llm(prompt)
    return [t.strip() for t in res.split(",")]

def call_mcp(tool, query):
    print("Inside call_mcp block")
    res = requests.post(MCP_URL, json={
        "tool": tool,
        "query": query
    })
    return res.json()["result"]

def handle_query(query):
    print("Inside handle_query block")
    tools = decide_tools(query)
    print("tools decided :", tools)
    context = ""
    for t in tools:
        context += f"\n[{t.upper()}]\n{call_mcp(t, query)}\n"

    return ask_llm(f"""
User Query: {query}

Context:
{context}

Give:
- Root cause
- Fix steps
""", max_tokens=300)