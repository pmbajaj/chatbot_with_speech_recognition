import argparse
import subprocess
import sys
import os
import platform
import threading
import time

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.terminal_chat import main as terminal_main

def get_npm_command():
    """Get the correct npm command based on the operating system"""
    if platform.system() == 'Windows':
        return 'npm.cmd'
    return 'npm'

def print_output(process, prefix):
    """Print output from a process with a prefix"""
    while True:
        output = process.stdout.readline()
        if output:
            print(f"{prefix}: {output.strip()}")
        error = process.stderr.readline()
        if error:
            print(f"{prefix} ERROR: {error.strip()}")
        if process.poll() is not None:
            break

def run_web_interface():
    """Run the web interface (both frontend and backend)"""
    try:
        print("\nInstalling frontend dependencies...")
        npm_command = get_npm_command()
        subprocess.run([npm_command, 'install'], cwd='frontend', check=True)
        
        print("\nStarting backend server...")
        backend_process = subprocess.Popen(
            [sys.executable, "backend/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start output monitoring threads
        backend_thread = threading.Thread(
            target=print_output,
            args=(backend_process, "Backend"),
            daemon=True
        )
        backend_thread.start()
        
        # Wait a bit for backend to start
        time.sleep(2)
        
        print("\nStarting frontend server...")
        frontend_process = subprocess.Popen(
            [npm_command, "start"],
            cwd="frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start output monitoring thread for frontend
        frontend_thread = threading.Thread(
            target=print_output,
            args=(frontend_process, "Frontend"),
            daemon=True
        )
        frontend_thread.start()
        
        print("\nStarting the web interface...")
        print("Backend server running at http://localhost:8000")
        print("Frontend server running at http://localhost:3000")
        print("\nPress Ctrl+C to stop both servers")
        
        # Wait for both processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\nError: Failed to start the frontend. Make sure Node.js and npm are installed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

def run_terminal_interface():
    """Run the terminal interface"""
    terminal_main()

def main():
    parser = argparse.ArgumentParser(description="NLP Chatbot Interface")
    parser.add_argument(
        "--mode",
        choices=["web", "terminal"],
        default="web",
        help="Choose the interface mode (web or terminal)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "web":
        run_web_interface()
    else:
        run_terminal_interface()

if __name__ == "__main__":
    main() 