from mcp.server.fastmcp import FastMCP
from mcp_server.tools.prometheus_tool import prometheus_tool
from mcp_server.tools.logs_tool import logs_tool
from mcp_server.tools.runbook_tool import runbook_tool
import psutil
import requests, os
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

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")



HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
@mcp.tool()
def list_repos(username: str) -> str:
    """
    List public repositories of a GitHub user.
    """

    try:
        url = f"https://api.github.com/users/{username}/repos"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return f"GitHub API Error: {response.text}"

        repos = response.json()

        if not repos:
            return "No repositories found."

        repo_names = [
            repo["name"]
            for repo in repos
        ]

        return "\n".join(repo_names)

    except requests.exceptions.Timeout:
        return "Request timed out."

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_recent_commits(owner: str, repo: str) -> str:
    """
    Get recent commits from a GitHub repository.
    """

    try:

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return f"GitHub API Error: {response.text}"

        commits = response.json()

        if not commits:
            return "No commits found."

        output = []

        for commit in commits[:5]:

            commit_info = f"""
Author: {commit['commit']['author']['name']}
Message: {commit['commit']['message']}
Date: {commit['commit']['author']['date']}
Commit URL: {commit['html_url']}
"""

            output.append(commit_info)

        return "\n".join(output)

    except Exception as e:
        return f"Error: {str(e)}"


JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

@mcp.tool()
def list_jenkins_jobs() -> str:
    """
    List Jenkins jobs.
    """

    try:

        url = f"{JENKINS_URL}/api/json"

        response = requests.get(
            url,
            auth=(JENKINS_USER, JENKINS_TOKEN),
            timeout=10
        )

        if response.status_code != 200:
            return f"Error: {response.text}"

        data = response.json()

        jobs = data.get("jobs", [])

        if not jobs:
            return "No Jenkins jobs found."

        output = []

        for job in jobs:
            output.append(
                f"Job: {job['name']}"
            )

        return "\n".join(output)

    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def trigger_build(
    job_name: str,
    username: str,
    run_tests: bool,
    env: str
) -> str:
    """
    Trigger parameterized Jenkins build.
    """

    try:

        url = f"{JENKINS_URL}/job/{job_name}/buildWithParameters"

        params = {
            "USERNAME": username,
            "RUN_TESTS": str(run_tests).lower(),
            "ENV": env
        }

        response = requests.post(
            url,
            auth=(JENKINS_USER, JENKINS_TOKEN),
            params=params,
            timeout=10
        )

        if response.status_code in [200, 201]:
            return (
                f"Build triggered successfully.\n"
                f"Job: {job_name}\n"
                f"USERNAME: {username}\n"
                f"RUN_TESTS: {run_tests}\n"
                f"ENV: {env}"
            )

        return (
            f"Failed to trigger build.\n"
            f"Status Code: {response.status_code}\n"
            f"Response: {response.text}"
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print("Token: ")
    print(os.getenv("GITHUB_TOKEN"))
    mcp.run()