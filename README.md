# 🛰️ SovereignC2

**SovereignC2** is a lightweight Command and Control (C2) framework developed for educational and research purposes, focusing on understanding adversarial communication, system interaction, and defensive analysis.

> ⚠️ This project is strictly for **educational use**, **lab environments**, and **authorized testing only**.

---

## 📌 Overview

SovereignC2 simulates a basic C2 infrastructure composed of:

* 🧠 **Agent (Client)** — Executes tasks on the target system
* 🌐 **Server (Controller)** — Manages agents and dispatches commands
* 🔌 **Task-based Communication Model** — Structured command execution flow
* 📦 **Modular Handlers** — Extensible functionality via action handlers

This project aims to demonstrate how C2 frameworks operate at a fundamental level, providing a base for further experimentation and improvement.

---

## ⚙️ Features

* Remote command execution (`cmd`, `shell`)
* System information gathering (`sysinfo`, `whoami`)
* Directory navigation (`cd`)
* File transfer (upload & download)
* Screenshot capture
* Task queue system
* Agent check-in mechanism
* Basic AES encryption support (server-side)
* Modular handler architecture

---

## 🏗️ Architecture

```
Agent  <---- HTTP ---->  Server
   |                       |
Executes tasks        Dispatches tasks
Returns results       Stores agents
```

### Flow:

1. Agent performs periodic **check-in**
2. Server responds with pending tasks
3. Agent executes tasks via handlers
4. Results are sent back to the server

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CATOMBO/SovereignC2.git
cd SovereignC2
```

---

### 2. Configure the server

Create your config file:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "server_url": "http://127.0.0.1:8080"
}
```

---

### 3. Run the server

```bash
python server.py
```

---

### 4. Run the agent

```bash
python agent.py
```

---

### 5. Send a test task

```bash
curl -X POST http://127.0.0.1:8080/task \
-H "Content-Type: application/json" \
-d '{"sid":"AGENT_ID","action":"whoami","params":{}}'
```

---

## 📂 Project Structure

```
SovereignC2/
├── agent/
│   ├── agent.py
│   ├── handlers/
│
├── server/
│   ├── server.py
│
├── protocol.json
├── config.example.json
└── README.md
```

---

## ⚠️ Limitations

This project is intentionally simplified and does not represent a fully operational or secure C2 framework.

Current limitations include:

- No authentication mechanism between agent and server  
- No persistent storage (in-memory only)  
- Partial encryption implementation (not enforced end-to-end)  
- Limited input validation and error handling  
- No agent integrity verification  
- No task prioritization or scheduling system  
- Basic communication model (HTTP polling only)  

These limitations are acknowledged and serve as opportunities for future improvements.

## 🔐 Security Notice

This project intentionally simplifies many aspects of real-world C2 frameworks.

Missing (by design or not yet implemented):

* Authentication between agent and server
* Persistent storage (database)
* Full encryption pipeline (agent ↔ server)
* Input validation hardening

---

## 🧠 Future Improvements

* Add agent authentication mechanism
* Implement persistent storage (SQLite/PostgreSQL)
* Full end-to-end encryption
* Web-based dashboard
* WebSocket communication
* Improved error handling and logging
* Advanced task scheduling
* Stealth and evasion techniques (for research purposes)

---

## ⚠️ Disclaimer

This project is intended **only for educational purposes**.

Do NOT use this software on systems you do not own or do not have explicit permission to test.

The author is not responsible for misuse or illegal activities.

---

## 👨‍💻 Author

Developed by **Calebe Araujo**

---

## 🎯 Why this project?

This project was built to explore and demonstrate core concepts behind Command and Control (C2) frameworks from a defensive and educational perspective.

Through this implementation, I focused on:

- Understanding how agents communicate with a central server  
- Designing a task-based execution model  
- Building a modular and extensible architecture  
- Exploring real-world trade-offs between functionality and security  
- Gaining hands-on experience with system interaction and remote operations  

Rather than replicating a full-featured C2, the goal was to create a clear, functional foundation that can be analyzed, extended, and improved over time.
