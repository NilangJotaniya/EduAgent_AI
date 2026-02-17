import subprocess
import requests
import time

OLLAMA_URL = "http://localhost:11434"


def is_ollama_running():
    try:
        requests.get(OLLAMA_URL, timeout=2)
        return True
    except:
        return False

def start_ollama():
    if is_ollama_running():
        print("✅ Ollama already running")
        return

    print("🚀 Starting Ollama server automatically...")

    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )

        for _ in range(15):
            if is_ollama_running():
                print("✅ Ollama started successfully")
                return
            time.sleep(1)

        print("❌ Ollama did not start")

    except Exception as e:
        print("⚠️ Error starting Ollama:", e)
