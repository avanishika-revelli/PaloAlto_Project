import subprocess
import sys
import os
import webbrowser
import time
import socket

PORT = 8501
URL = f"http://localhost:{PORT}"

def wait_for_server(port, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False

def main():
    # Launch Streamlit ONCE
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        f"--server.port={PORT}"
    ])

    # Open browser once server is ready
    if wait_for_server(PORT):
        webbrowser.open(URL)

    # IMPORTANT: DO NOT loop, DO NOT relaunch
    time.sleep(999999)

if __name__ == "__main__":
    main()
