# Create a setup script for easy installation
setup_content = '''#!/usr/bin/env python3
"""
Setup script for AI-Driven Adaptive Testing Platform
Run this script to quickly set up the application.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing packages")
        return False

def setup_env_file():
    """Set up environment file with API key"""
    env_file = ".env"
    example_file = ".env.example"
    
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists(example_file):
        # Create example file if it doesn't exist
        with open(example_file, "w") as f:
            f.write("OR_API_KEY=your_openrouter_api_key_here\\n")
    
    print("🔑 Setting up API key...")
    print("   You need an OpenRouter API key from: https://openrouter.ai/keys")
    
    api_key = input("   Enter your OpenRouter API key (or press Enter to skip): ").strip()
    
    if api_key:
        with open(env_file, "w") as f:
            f.write(f"OR_API_KEY={api_key}\\n")
        print("✅ API key saved to .env file")
    else:
        print("⚠️  Skipping API key setup")
        print("   You'll need to create .env file manually before running the app")
    
    return True

def main():
    """Main setup function"""
    print("🧠 AI-Driven Adaptive Testing Platform Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup environment
    if not setup_env_file():
        return False
    
    print("\\n🎉 Setup complete!")
    print("\\n📋 Next steps:")
    print("   1. Make sure your .env file has your OpenRouter API key")
    print("   2. Run: streamlit run app.py")
    print("   3. Upload a PDF and start testing!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
'''

with open("setup.py", "w") as f:
    f.write(setup_content)

print("Created setup.py script")