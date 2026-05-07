from mcp.server.fastmcp import FastMCP
from mcp_server.tools.prometheus_tool import prometheus_tool
from mcp_server.tools.logs_tool import logs_tool
from mcp_server.tools.runbook_tool import runbook_tool

mcp = FastMCP("Observability Server")

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

if __name__ == "__main__":
    mcp.run()