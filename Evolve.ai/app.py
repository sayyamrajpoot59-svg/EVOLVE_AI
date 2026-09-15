# app.py - Evolve Labs Master Web GUI Dashboard Core
import os
import json
from flask import Flask, render_template, request, jsonify
from chat_engine import chat_with_nova, BRAND_NAME
from code_fixer import analyze_and_fix_code
from sdlc_engine import generate_and_deploy_web_app

app = Flask(__name__)

ACTION_HISTORY = []
AGENT_TASKS = [
    {"id": 1, "agent": "LiveServerGuardian", "task": "Monitor server health and auto-patch errors", "status": "Active & Watching"},
    {"id": 2, "agent": "Apex-CodeHandler", "task": "Audit and refactor core modules", "status": "Ready"}
]

@app.route("/")
def index():
    return render_template("dashboard.html", brand=BRAND_NAME)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Please provide a message."})
    response = chat_with_nova(user_message)
    return jsonify({"response": response})

@app.route("/api/sdlc", methods=["POST"])
def api_sdlc():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"status": "error", "report": "Please provide software requirements."})
    text, files = generate_and_deploy_web_app(prompt)
    return jsonify({"status": "success", "report": text, "files": files})

@app.route("/api/fix_code", methods=["POST"])
def api_fix_code():
    data = request.json or {}
    file_path = data.get("file_path", "")
    issue = data.get("issue", "")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "Invalid or non-existent file path."})
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            old_code = f.read()
        ACTION_HISTORY.append({"file_path": file_path, "backup_code": old_code})
    except Exception:
        pass
    result = analyze_and_fix_code(file_path, issue)
    return jsonify({"status": "success", "report": result})

@app.route("/api/undo_action", methods=["POST"])
def api_undo_action():
    if not ACTION_HISTORY:
        return jsonify({"status": "error", "message": "No actions to undo."})
    last_action = ACTION_HISTORY.pop()
    file_path = last_action["file_path"]
    backup_code = last_action["backup_code"]
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(backup_code)
        return jsonify({"status": "success", "message": f"Successfully reverted changes on '{file_path}'!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/tasks", methods=["GET", "POST"])
def api_tasks():
    global AGENT_TASKS
    if request.method == "POST":
        data = request.json or {}
        new_task = {
            "id": len(AGENT_TASKS) + 1,
            "agent": data.get("agent", "CustomAgent"),
            "task": data.get("task", ""),
            "status": "In Progress"
        }
        AGENT_TASKS.append(new_task)
        return jsonify({"status": "success", "task": new_task})
    return jsonify({"tasks": AGENT_TASKS})

if __name__ == "__main__":
    print(f"[*] Starting {BRAND_NAME} Enterprise Web GUI Dashboard...")
    app.run(host="127.0.0.1", port=5000, debug=True)