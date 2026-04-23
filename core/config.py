import json
import os
from typing import Dict, Any

class AgentConfig:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                
        else:
            self.config ={"server_url": "https://127.0.0.1:8080",
                          "server_host": "127.0.0.1",
                          "server_port": 8080,
                          "sleep_time": 5,
                          "jitter": 2,
                          "agent_id": None}
            self.save_config()
            
    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
            
    def get(self, key: str, default=None):
        return self.config.get(key,default)
    
    def set(self, key: str, value):
        self.config[key] = value
        self.save_config()