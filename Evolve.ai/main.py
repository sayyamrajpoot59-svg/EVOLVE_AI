# main.py - Evolve Labs Master Control Hub & Autonomous Orchestrator
import os
import sys
from sdlc_engine import generate_and_deploy_web_app
from chat_engine import chat_with_nova, BRAND_NAME
from code_fixer import analyze_and_fix_code
from evolution_studio import EvolveAgentStudio, initialize_default_enterprise_agents

def print_banner():
    print("=" * 60)
    print(f"      {BRAND_NAME} - Autonomous AI Agent & SDLC Platform")
    print("      'Your Elite Enterprise AI Engineering & Operations Hub'")
    print("=" * 60)

def main_menu():
    # Ensure default enterprise agents exist
    initialize_default_enterprise_agents()
    studio = EvolveAgentStudio()

    while True:
        print_banner()
        print("\n[ Master Control Dashboard ]")
        print("1. Chat with Nova (Personal Right-Hand & System Assistant)")
        print("2. Autonomous Code Bug Fixer & Auto-Writer (Scan & Patch Files)")
        print("3. Agent Studio & Live Surveillance (LiveServerGuardian & Custom Agents)")
        print("4. Agentic SDLC Web App Generator (Coming Next: Build & Deploy to Localhost with Admin)")
        print("5. Exit Evolve Labs")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print(f"\n--- Entering Nova AI Chat Core ---")
            print("Type 'exit' or 'back' to return to main menu.\n")
            while True:
                user_msg = input("Rana > ").strip()
                if user_msg.lower() in ['exit', 'back', 'quit']:
                    break
                if not user_msg:
                    continue
                response = chat_with_nova(user_msg)
                print(f"\n{BRAND_NAME} > {response}\n" + "-"*40)

        elif choice == '2':
            print(f"\n--- Autonomous Bug Fixer Module ---")
            target = input("Enter target file path (e.g. test_buggy.py): ").strip()
            if target:
                issue = input("Describe bug/task (Press Enter for full audit): ").strip()
                result = analyze_and_fix_code(target, issue)
                print(f"\n{result}\n")
            input("Press Enter to continue...")

        elif choice == '3':
            print(f"\n--- Agent Studio & Live Monitor ---")
            print("1. Run LiveServerGuardian (Check live app/server logs)")
            print("2. Run NovaAssistant")
            print("3. List All Active Agents")
            sub_choice = input("Select option (1-3): ").strip()
            
            if sub_choice == '1':
                logs = input("Paste live server logs or error traces: ").strip()
                print("\n[LiveServerGuardian Analyzing...]")
                print(studio.run_agent_task("LiveServerGuardian", logs))
            elif sub_choice == '2':
                task = input("What should Nova assist with? ").strip()
                print(studio.run_agent_task("NovaAssistant", task))
            elif sub_choice == '3':
                print(f"\nActive Agents in Registry: {list(studio.agents.keys())}\n")
            input("Press Enter to continue...")

        elif choice == '4':
            print(f"\n--- Agentic SDLC Web App Generator ---")
            req_prompt = input("Enter software requirements (e.g., Build a pet supply store with admin login): ").strip()
            if req_prompt:
                response_text, saved_files = generate_and_deploy_web_app(req_prompt)
                print(f"\n[+] Generated Files Successfully Saved: {saved_files}")
                print(f"--------------------------------------------------")
            input("Press Enter to continue...")

        elif choice == '5':
            print(f"\nShutting down {BRAND_NAME}. Allah Hafiz, Rana!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please select between 1 and 5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()