import subprocess

def logs_tool(query):
    cmd = ["log", "show", "--last", "1m"]
    logs = subprocess.check_output(cmd, text=True)
    return logs[:2000]   # limit