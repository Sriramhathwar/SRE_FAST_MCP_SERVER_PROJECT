import requests
from mcp_server.utils.promql_generator import generate_promql
from mcp_server.utils.validator import validate_promql

PROM_URL = "http://localhost:9090/api/v1/query"

def prometheus_tool(query):
    print("Inside prometheus_tool block")
    promql = generate_promql(query)

    if not validate_promql(promql):
        return "Invalid PromQL"

    res = requests.get(PROM_URL, params={"query": promql})
    return f"PromQL: {promql}\nResult: {res.json()}"