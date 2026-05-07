from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp_server.tools.prometheus_tool import prometheus_tool
from mcp_server.tools.logs_tool import logs_tool
from mcp_server.tools.runbook_tool import runbook_tool

app = FastAPI()
mcp = FastMCP("Observability Server")

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


    # MCP tools for Claude
@mcp.tool()
def metrics(query: str) -> str:
    """Query Prometheus metrics"""
    return prometheus_tool(query)

@mcp.tool()
def logs(query: str) -> str:
    """Fetch logs"""
    return logs_tool(query)

@mcp.tool()
def runbook(query: str) -> str:
    """Look up runbook information"""
    return runbook_tool(query)

# Mount MCP as SSE on the FastAPI app
app.mount("/sse", mcp.sse_app())