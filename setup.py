import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 9 or version.minor > 11:
        print("Error: Python version must be between 3.9 and 3.11")
        print(f"Current version: {sys.version}")
        sys.exit(1)

def install_dependencies():
    print("Installing dependencies...")
    
    # First, upgrade pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install wheel
    subprocess.check_call([sys.executable, "-m", "pip", "install", "wheel"])
    
    # Install numpy first (required for other packages)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])
    
    # Install torch separately (with CPU version for Windows)
    if platform.system() == "Windows":
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.1.2", "--index-url", "https://download.pytorch.org/whl/cpu"])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.1.2"])
    
    # Install the rest of the requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Download spaCy model
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    print("\nDependencies installed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Run the chatbot using: python run.py --mode web")
    print("   or")
    print("   python run.py --mode terminal")

def main():
    # Check Python version first
    check_python_version()
    
    # Install dependencies
    install_dependencies()

if __name__ == "__main__":
    main() 