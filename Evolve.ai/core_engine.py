# core_engine.py - Revolve AI Full-Stack Autonomous Autonomous Software Engineering Agent v2.1
import os
import json
import urllib.request
import urllib.error
import ssl
import time
from datetime import datetime

# ================= CONFIGURATION =================
GEMINI_API_KEY = ""
MODEL_NAME = "gemini-3.5-flash"  # Ya gemini-1.5-flash agar 3.8 busy ho
HISTORY_FILE = "user_history.json"

# ================= 1. SECURITY & SANITIZATION MODULE =================
def sanitize_project_name(raw_name):
    """Folder name ko Windows-friendly aur safe banata hai"""
    safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in raw_name).strip().replace(' ', '_')
    return safe_name if safe_name else "generated_project"

# ================= 2. DATA & HISTORY LOGGING MODULE =================
def log_activity(prompt_text, project_name, status):
    """User aur project ki activity ko history file mein record karta hai"""
    history_data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        except Exception:
            history_data = []
            
    history_data.append({
        "user_prompt": prompt_text,
        "project_name": project_name,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)

def show_history():
    """Terminal par purani history print karta hai"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            hist = json.load(f)
        print("\n================ REVOLVE AI PROJECT HISTORY ================")
        for idx, h in enumerate(hist, 1):
            print(f"{idx}. Time: {h['timestamp']} | Status: [{h['status']}]")
            print(f"   Project Folder: {h['project_name']}")
            print(f"   Task: {h['user_prompt']}")
            print("-" * 60)
    else:
        print("\nAbhi tak koi history maujood nahi hai.")

# ================= 3. AI AGENT COMMUNICATION & CODE GENERATION MODULE =================
def request_ai_code(prompt_description):
    """Gemini API se contact karke full-stack code generate karwata hai (Zero Dummy Code Rule)"""
    full_prompt = (
        "You are Revolve AI, an elite autonomous full-stack software engineering agent. "
        "The user demands a fully working, production-grade software with ZERO dummy code or dead buttons. "
        "CRITICAL RULES:\n"
        "1. Every single button, menu, form, and interactive element MUST have real backend or client-side logic attached. "
        "No empty click handlers, no alert('Coming soon') placeholders, and no unlinked features.\n"
        "2. If it's a data tool (like Profit/SKU calculator), implement real CSV export, data calculation, and local storage/file saving.\n"
        "3. If it's a chat or utility app, implement real state management (e.g., New Chat creation, history logging, active session handling).\n"
        "4. Provide complete, robust source code across all necessary files (e.g., main logic, backend handlers, UI, styling, and a working 'run.bat' script).\n"
        "Format your response strictly as valid JSON where keys are file names (including subpaths like 'css/styles.css' or 'templates/index.html') "
        "and values are the complete source code. Do not include markdown code block ticks like ```json or ```, just return raw JSON text.\n\n"
        f"User Task Description: {prompt_description}"
    )

    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }

    max_retries = 3
    retry_delay = 5

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Revolve AI full-stack architecture aur backend logic compile kar raha hai... (Koshish {attempt}/{max_retries})")
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
            ssl_context = ssl._create_unverified_context()
            
            with urllib.request.urlopen(req, context=ssl_context) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                
                raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:-3].strip()
                elif raw_text.startswith("```"):
                    raw_text = raw_text[3:-3].strip()

                return json.loads(raw_text)

        except urllib.error.HTTPError as e:
            error_detail = e.read().decode("utf-8")
            print(f"Google API HTTP Error {e.code}: {error_detail}")
            if e.code in [503, 429] and attempt < max_retries:
                print(f"Server busy hai. {retry_delay} seconds baad khud dobara koshish ki ja rahi hai...")
                time.sleep(retry_delay)
                retry_delay *= 2 
            else:
                return None
        except Exception as e:
            print(f"General Error aa gaya: {e}")
            return None

    return None

# ================= 4. PROJECT BUILDER & LAUNCHER MODULE =================
def build_project(project_name, prompt_description):
    safe_name = sanitize_project_name(project_name)
    
    if not os.path.exists(safe_name):
        os.makedirs(safe_name)
        print(f"Folder '{safe_name}' successfully ban gaya hai!")
    else:
        print(f"Folder '{safe_name}' pehle se maujood hai.")

    files_data = request_ai_code(prompt_description)
    
    if not files_data:
        print("\n[!] Code generate nahi ho saka.")
        log_activity(prompt_description, safe_name, "FAILED")
        return False, safe_name

    try:
        for file_name, file_content in files_data.items():
            file_path = os.path.join(safe_name, file_name)
            
            # Subfolders (jaise css/ ya templates/) ko automatically create karne ka logic
            file_dir = os.path.dirname(file_path)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            print(f"Generated Fully-Wired Asset -> {file_path}")

        bat_path = os.path.join(safe_name, "run.bat")
        if not os.path.exists(bat_path):
            with open(bat_path, "w", encoding="utf-8") as bat_file:
                bat_file.write("@echo off\ncls\necho Revolve AI Full-Stack App Launcher...\npython main.py || start index.html\npause")

        log_activity(prompt_description, safe_name, "SUCCESS")
        print(f"\n🎉 Mukammal Full-Stack Software tayar ho gaya hai!")
        return True, safe_name

    except Exception as e:
        print(f"File writing error: {e}")
        log_activity(prompt_description, safe_name, "FAILED_FILE_WRITE")
        return False, safe_name

# ================= 5. MAIN INTERACTIVE CLI INTERFACE =================
if __name__ == "__main__":
    print("=== Revolve AI: Full-Stack Autonomous Software Engineering Agent v2.1 ===")
    while True:
        p_name = input("\nProject ka folder naam likhein (ya 'history', 'exit'): ").strip()
        
        if p_name.lower() == 'exit':
            print("Revolve AI band ho raha hai. Allah Hafiz!")
            break
            
        if p_name.lower() == 'history':
            show_history()
            continue
            
        p_desc = input("Aapko kaisa professional software/game banwana hai? (Detail mein likhein - sabhi buttons aur backend requirements lazmi mention karein): ").strip()
        if not p_desc:
            print("Task khali nahi ho sakta!")
            continue
            
        success, folder_name = build_project(p_name, p_desc)
        
        if success:
            # Interactive Post-Build Feedback Loop
            while True:
                print("\n--- Post-Build Review ---")
                feedback = input("Kya yeh software bilkul theek bana hai aur iske saare buttons kaam kar rahe hain? (Agar kuch change ya fix karwana hai toh yahan likhein, warna 'done' likhein): ").strip()
                
                if feedback.lower() == 'done':
                    print("Behtareen! Software save ho chuka hai.")
                    break
                else:
                    print(f"Revolve AI aapki di gayi correction '{feedback}' ke mutabiq code patch kar raha hai...")
                    success, folder_name = build_project(p_name, f"{p_desc} | CORRECTION & FIX REQUESTED BY USER: {feedback}")
                    if success:
                        print("Patch successfully apply ho gaya hai!")
            
            preview = input("\nKya aap is software ko abhi run karke check karna chahte hain? (y/n): ").strip().lower()
            if preview == 'y':
                print(f"'{folder_name}' folder khul raha hai...")
                try:
                    os.startfile(folder_name)
                except Exception:
                    pass