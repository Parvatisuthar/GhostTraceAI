import subprocess
import sys
import os

def run_streamlit():
    dashboard_app = os.path.join("dashboard", "app.py")

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        dashboard_app
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    print("👻 Launching GhostTrace AI Dashboard...")
    run_streamlit()