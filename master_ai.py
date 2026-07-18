import sys, time, os, subprocess
from datetime import datetime

# --- CONFIGURATION ---
AI_NAME = "PROJECT MANAGER"
MODEL = "deepseek-r1:1.5b"
USER = "Admin"
HISTORY_DIR = "chat_history"
REPO_NAME = "my-ultimate-ai"  # We gave it a cool new name

# --- COLORS ---
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

if not os.path.exists(HISTORY_DIR): os.makedirs(HISTORY_DIR)
current_log_file = f"{HISTORY_DIR}/chat_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

def type_header(text, color=GREEN):
    print(color + BOLD + f"[{AI_NAME}]: " + RESET + color + text + RESET)

def log_to_file(speaker, text):
    with open(current_log_file, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {speaker}: {text}\n")

# --- THE HANDS & MUSCLES ---
def use_hands(action, value=""):
    type_header(f"Activating HANDS -> {action}...", color=MAGENTA)
    if action == "speak": subprocess.run(["say", value])
    elif action == "volume": subprocess.run(["osascript", "-e", f"set volume output volume {value}"])

def use_muscles():
    type_header("Flexing MUSCLES (Swift) -> Hardware Scan...", color=YELLOW)
    subprocess.run(["swift", "muscles.swift"])

# --- THE AGGRESSIVE UPLOADER ☁️ ---
def upload_to_github():
    type_header("Initializing FORCE UPLOAD Sequence...", color=CYAN)
    
    # 1. Login Check
    if subprocess.call(["gh", "auth", "status"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        type_header("Error: Not logged in. Run 'gh auth login' first!", color=RED)
        return

    # 2. Re-Initialize Git
    if os.path.exists(".git"):
        # If git exists, we add everything
        os.system("git add .")
        os.system('git commit -m "Auto-Update"')
    else:
        # If new, we start fresh
        type_header("Creating fresh repository...", color=GREEN)
        os.system("git init")
        os.system("git branch -m main")
        os.system("git add .")
        os.system('git commit -m "Initial AI Upload"')

    # 3. FORCE CREATE & PUSH
    type_header(f"Pushing to GitHub: {REPO_NAME}...", color=CYAN)
    
    # Try to create the repo. If it fails (exists), it continues.
    os.system(f"gh repo create {REPO_NAME} --public --source=. --push 2>/dev/null")
    
    # The Magic Line: --force ensures it works even if there are conflicts
    push_success = os.system("git push -u origin main --force")
    
    if push_success == 0:
        username = subprocess.check_output("gh api user -q .login", shell=True).decode().strip()
        type_header(f"✅ SUCCESS! Live at: https://github.com/{username}/{REPO_NAME}", color=GREEN)
        subprocess.run(["open", f"https://github.com/{username}/{REPO_NAME}"])
    else:
        type_header("Upload failed. Check your internet.", color=RED)

# --- THE BRAIN ---
def ask_deepseek(prompt):
    type_header("Thinking...", color=CYAN)
    log_to_file(USER, prompt)
    print(CYAN + "----------------------------------------" + RESET)
    process = subprocess.Popen(["ollama", "run", MODEL, prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    full_response = ""
    while True:
        output = process.stdout.read(1)
        if output == '' and process.poll() is not None: break
        if output:
            sys.stdout.write(CYAN + output + RESET)
            sys.stdout.flush()
            full_response += output
    print(CYAN + "\n----------------------------------------" + RESET)
    log_to_file(AI_NAME, full_response)

def main():
    os.system("clear")
    print(GREEN + "========================================")
    print(f"   PROJECT MANAGER ONLINE: {AI_NAME}")
    print("========================================" + RESET)

    while True:
        try:
            print("")
            user_input = input(f"{YELLOW}{USER} > {RESET}").strip()
            if user_input.lower() in ["exit", "quit"]: break

            if user_input.lower() == "upload": upload_to_github()
            elif user_input.lower() == "status": use_muscles()
            elif user_input.lower().startswith("volume "): use_hands("volume", user_input.split(" ")[-1])
            elif user_input.lower() == "game":
                if os.path.exists("minecraft3d.py"):
                    type_header("Launching Game...", color=GREEN)
                    subprocess.run(["python3", "minecraft3d.py"])
            else: ask_deepseek(user_input)

        except KeyboardInterrupt: break

if __name__ == "__main__":
    main()
