from mcp.server.fastmcp import FastMCP
from mcp_server.tools.prometheus_tool import prometheus_tool
from mcp_server.tools.logs_tool import logs_tool
from mcp_server.tools.runbook_tool import runbook_tool
import psutil
import socket
import ssl
from datetime import datetime
import subprocess

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

@mcp.tool()
def get_memory_usage() -> str:
    """Get current memory usage."""
    mem = psutil.virtual_memory()

    return (
        f"Total: {round(mem.total / (1024**3), 2)} GB\n"
        f"Used: {round(mem.used / (1024**3), 2)} GB\n"
        f"Usage: {mem.percent}%"
    )

@mcp.tool()
def disk_usage(path: str = "/") -> str:
    """Get disk usage for a path."""

    disk = psutil.disk_usage(path)

    return (
        f"Path: {path}\n"
        f"Total: {round(disk.total / (1024**3), 2)} GB\n"
        f"Used: {round(disk.used / (1024**3), 2)} GB\n"
        f"Free: {round(disk.free / (1024**3), 2)} GB\n"
        f"Usage: {disk.percent}%"
    )

@mcp.tool()
def top_processes(limit: int = 5) -> str:
    """Get top CPU consuming processes."""

    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append(proc.info)

    top = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

    output = []

    for p in top[:limit]:
        output.append(
            f"PID: {p['pid']} | Name: {p['name']} | CPU: {p['cpu_percent']}%"
        )

    return "\n".join(output)

@mcp.tool()
def check_port(host: str, port: int) -> str:
    """Check if a port is open."""

    s = socket.socket()

    result = s.connect_ex((host, port))

    s.close()

    if result == 0:
        return f"Port {port} is OPEN on {host}"

    return f"Port {port} is CLOSED on {host}"

@mcp.tool()
def ssl_expiry(hostname: str, port: int = 443) -> str:
    """Get SSL certificate expiry."""

    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:

            cert = ssock.getpeercert()

            expiry = cert['notAfter']

            expiry_date = datetime.strptime(
                expiry,
                '%b %d %H:%M:%S %Y %Z'
            )

            days_left = (expiry_date - datetime.utcnow()).days

            return (
                f"Hostname: {hostname}\n"
                f"Expiry Date: {expiry_date}\n"
                f"Days Left: {days_left}"
            )
        

@mcp.tool()
def run_command(command: str) -> str:
    """Run shell command."""

    result = subprocess.check_output(
        command,
        shell=True,
        text=True
    )

    return result


if __name__ == "__main__":
    mcp.run()