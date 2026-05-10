from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp_server.tools.prometheus_tool import prometheus_tool
from mcp_server.tools.logs_tool import logs_tool
from mcp_server.tools.runbook_tool import runbook_tool

app = FastAPI()

@app.post("/mcp")
def handle_mcp(req: dict):
    print("Inside handle_mcp block")
    tool = req.get("tool")
    query = req.get("query", "")
    print("Tool:", tool)
    if tool == "metrics":
        print("Inside hmetrics")
        return {"result": prometheus_tool(query)}

    elif tool == "logs":
        print("Inside logs")
        return {"result": logs_tool(query)}

    elif tool == "runbook":
        print("Inside runbook")
        return {"result": runbook_tool(query)}

    return {"result": "Unknown tool"}


    