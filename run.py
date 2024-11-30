import subprocess
import sys
import time
import os


def run_frontend():
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
        if os.name == 'nt':  # Windows
            subprocess.Popen(['npm.cmd', 'run', 'dev'], cwd=frontend_path, shell=True)
        else:  # Unix/Linux/MacOS
            subprocess.Popen(['npm', 'run', 'dev'], cwd=frontend_path)
    except Exception as e:
        print(f"Error starting frontend: {e}")
        sys.exit(1)


def run_backend():
    try:
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, 'app.py'], cwd=backend_path, shell=True)
        else:  # Unix/Linux/MacOS
            subprocess.Popen([sys.executable, 'app.py'], cwd=backend_path)
    except Exception as e:
        print(f"Error starting backend: {e}")
        sys.exit(1)


if __name__ == '__main__':
    print("Starting backend server...")
    run_backend()
    time.sleep(2)  # Wait for backend to start

    print("Starting frontend server...")
    run_frontend()

    print("\nBoth servers are running!")
    print("Frontend: http://localhost:5173")  # Vite uses port 5173 by default
    print("Backend: http://localhost:5000")
    print("\nPress Ctrl+C to stop both servers")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)