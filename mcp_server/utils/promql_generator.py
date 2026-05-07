from agent.llm import ask_llm

def generate_promql(query):
    print("Inside generate_promql block")
    prompt = f"""
Convert user query to PromQL.

Examples:
CPU usage → rate(node_cpu_seconds_total[1m])
Memory usage → node_memory_MemAvailable_bytes

Query: {query}
PromQL:
"""
    return ask_llm(prompt, max_tokens=100)