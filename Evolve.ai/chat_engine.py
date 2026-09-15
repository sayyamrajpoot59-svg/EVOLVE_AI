# chat_engine.py - Evolve Labs Core Configuration & Chat Engine
import json
import urllib.request
import ssl

# ================= CONFIGURATION =================
# Apni asal Gemini API key yahan paste karein
GEMINI_API_KEY = ""
CHAT_MODEL = "gemini-3.5-flash"  # Ya jo model aap use kar rahe hain
BRAND_NAME = "Evolve Labs"
# =================================================

def chat_with_nova(user_message):
    """
    Sends user message to Gemini API with Nova's system persona
    and returns the AI's response string.
    """
    system_instruction = (
        f"You are {BRAND_NAME}'s core AI Companion and Right-Hand Assistant ('Nova') created for Rana Sayyam. "
        "You manage daily workflows, organize technical tasks, write scripts, and help orchestrate "
        "full computer automation and system management tasks with extreme precision and wit."
    )

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_message}]}
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
                return "[!] Model ne koi response return nahi kiya."
                
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                return "[!] Response parts khali hain."
                
            return parts[0].get("text", "").strip()
            
    except Exception as e:
        return f"[!] Chat API Error: {str(e)}"