# sdlc_engine.py - Evolve Labs Agentic SDLC Web App Generator Core
import os
import json
import urllib.request
import ssl
import re
from chat_engine import GEMINI_API_KEY, CHAT_MODEL, BRAND_NAME

def generate_and_deploy_web_app(requirement_prompt):
    """
    Takes user software requirements, generates a complete Flask web application
    with auto-admin credentials and UI templates, saves it to a local folder,
    and provides local execution details.
    """
    print(f"\n[Evolve SDLC Agent] Analyzing requirements and architecting web application...")

    system_instruction = (
        f"You are {BRAND_NAME}'s elite Autonomous Software Architect and Full-Stack SDLC Agent. "
        "Your job is to build a complete, self-contained Flask web application based on the user's requirements. "
        "CRITICAL REQUIREMENTS FOR THE GENERATED APP:\n"
        "1. Use Flask as the backend framework.\n"
        "2. Automatically create an SQLite database with an Admin user pre-configured (Username: admin, Email: admin@evolvelabs.local, and a secure generated password).\n"
        "3. Include both backend python code (`app.py`) and HTML frontend templates (`templates/index.html`).\n"
        "4. Format your response clearly using markdown file headers like `### FILE: app.py` followed by ```python ... ``` and `### FILE: templates/index.html` followed by ```html ... ```.\n"
        "5. Ensure the code is clean, production-ready, and runs out-of-the-box on localhost."
    )

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": f"Build a complete web application for this requirement: {requirement_prompt}"}]}
        ]
    }

    url = f"https://generativelanguage.googleapis.com/v1/models/{CHAT_MODEL}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        ctx = ssl._create_unverified_context()
        
        with urllib.request.urlopen(req, context=ctx) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            
            candidates = res_json.get("candidates", [])
            if not candidates:
                return "[!] Model returned no architecture candidates.", []
                
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return "[!] Response parts are empty.", []
                
            response_text = parts[0].get("text", "").strip()
            
            # Parse and save files to workspace directory
            output_dir = "generated_projects"
            saved_files = parse_and_save_sdlc_output(response_text, output_dir)
            return response_text, saved_files

    except Exception as e:
        return f"[!] SDLC Generation Error: {str(e)}", []

def parse_and_save_sdlc_output(response_text, base_dir):
    """Extracts files based on markdown file headers and saves them locally."""
    saved = []
    os.makedirs(base_dir, exist_ok=True)
    
    pattern = r"###\s*FILE:\s*([^\n]+)\s*```(?:\w+)?\s*([\s\S]*?)```"
    matches = re.findall(pattern, response_text)
    
    if matches:
        for filepath, code_content in matches:
            filepath = filepath.strip()
            full_path = os.path.join(base_dir, filepath)
            dir_name = os.path.dirname(full_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(code_content.strip())
            saved.append(full_path)
    else:
        # Fallback: extract python blocks if explicit file headers weren't used
        py_pattern = r"```python\s*([\s\S]*?)```"
        py_matches = re.findall(py_pattern, response_text)
        if py_matches:
            full_path = os.path.join(base_dir, "app.py")
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(py_matches[0].strip())
            saved.append(full_path)
            
    return saved