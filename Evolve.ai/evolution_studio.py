# evolution_studio.py - Evolve Labs Master Agent Studio & Live Monitor Core
import os
import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from chat_engine import GEMINI_API_KEY, CHAT_MODEL, BRAND_NAME

class EvolveAgentStudio:
    def __init__(self):
        self.agents_db_file = "evolve_agents.json"
        self.load_agents()

    def load_agents(self):
        if os.path.exists(self.agents_db_file):
            try:
                with open(self.agents_db_file, "r", encoding="utf-8") as f:
                    self.agents = json.load(f)
            except Exception:
                self.agents = {}
        else:
            self.agents = {}

    def save_agents(self):
        with open(self.agents_db_file, "w", encoding="utf-8") as f:
            json.dump(self.agents, f, indent=4)

    def create_agent(self, agent_name, agent_role, system_prompt):
        """Creates a custom specialized AI agent for the client."""
        self.agents[agent_name] = {
            "role": agent_role,
            "system_prompt": system_prompt,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_agents()
        return f"[+] Agent '{agent_name}' ({agent_role}) successfully created in Evolve Studio!"

    def run_agent_task(self, agent_name, task_input):
        """Executes a task using a specific custom agent."""
        if agent_name not in self.agents:
            return f"[!] Error: Agent '{agent_name}' exist nahi karta. Pehle create karein."
        
        agent_info = self.agents[agent_name]
        system_instruction = agent_info["system_prompt"]
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [
                {"role": "user", "parts": [{"text": task_input}]}
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
                    return "[!] Agent ne koi response return nahi kiya."
                
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts:
                    return "[!] Agent response parts are empty."
                    
                return parts[0].get("text", "").strip()
        except Exception as e:
            return f"[!] Agent Execution Error: {str(e)}"

# ================= PRE-BUILT ENTERPRISE AGENTS SETUP =================
def initialize_default_enterprise_agents():
    studio = EvolveAgentStudio()
    
    # 1. Live Software & App Surveillance Agent
    studio.create_agent(
        agent_name="LiveServerGuardian",
        agent_role="Live Software & Uptime Surveillance Specialist",
        system_prompt=(
            f"You are {BRAND_NAME}'s elite Live Surveillance Agent ('LiveServerGuardian'). "
            "Your core job is to monitor live software, web applications, and APIs. "
            "Analyze server logs, HTTP response codes, latency metrics, and error triggers provided by the user. "
            "Instantly diagnose whether a live issue is a database crash, frontend timeout, or network error, "
            "and provide immediate emergency mitigation steps and patch scripts."
        )
    )

    # 2. Personal Right-Hand Assistant ('Nova')
    studio.create_agent(
        agent_name="NovaAssistant",
        agent_role="Personal Executive & System Control Assistant",
        system_prompt=(
            f"You are {BRAND_NAME}'s core AI Companion and Right-Hand Assistant ('Nova') created for Rana Sayyam. "
            "You manage daily workflows, organize technical tasks, write scripts, and help orchestrate "
            "full computer automation and system management tasks with extreme precision and wit."
        )
    )
    print("[+] Evolve Labs Enterprise Agents ('LiveServerGuardian' & 'NovaAssistant') initialized successfully!")

if __name__ == "__main__":
    print(f"==================================================")
    print(f"  {BRAND_NAME} - Agent Studio & Live Monitor Core")
    print(f"==================================================")
    
    # Initialize default enterprise agents on first run
    initialize_default_enterprise_agents()
    
    studio = EvolveAgentStudio()
    
    while True:
        print("\nSelect Action:")
        print("1. Run LiveServerGuardian (Check live app/server logs & status)")
        print("2. Run NovaAssistant (Personal right-hand help)")
        print("3. Create Custom Agent")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            log_data = input("Paste live server logs, error trace, or app status details: ").strip()
            print("\n[LiveServerGuardian is analyzing live environment...]")
            response = studio.run_agent_task("LiveServerGuardian", log_data)
            print(f"\n[Guardian Report]:\n{response}\n" + "-"*50)
            
        elif choice == '2':
            task = input("What do you want Nova to assist you with? ").strip()
            print("\n[NovaAssistant is processing...]")
            response = studio.run_agent_task("NovaAssistant", task)
            print(f"\n[Nova Reply]:\n{response}\n" + "-"*50)
            
        elif choice == '3':
            name = input("Enter Agent Name (e.g. BugFixerPro): ").strip()
            role = input("Enter Agent Role: ").strip()
            prompt = input("Enter System Instruction/Behavior Prompt: ").strip()
            res = studio.create_agent(name, role, prompt)
            print(res)
            
        elif choice == '4':
            print("Exiting Agent Studio. Allah Hafiz!")
            break
        else:
            print("[!] Invalid choice. Try again.")