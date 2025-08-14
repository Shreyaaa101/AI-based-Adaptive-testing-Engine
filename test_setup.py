#!/usr/bin/env python3
"""
Test script for AI-Driven Adaptive Testing Platform
Run this to verify that all components are working properly.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported"""
    print("📦 Testing package imports...")

    try:
        import streamlit
        print(f"   ✅ Streamlit: {streamlit.__version__}")
    except ImportError as e:
        print(f"   ❌ Streamlit import failed: {e}")
        return False

    try:
        import requests
        print(f"   ✅ Requests: {requests.__version__}")
    except ImportError as e:
        print(f"   ❌ Requests import failed: {e}")
        return False

    try:
        import fitz
        print(f"   ✅ PyMuPDF: {fitz.__version__}")
    except ImportError as e:
        print(f"   ❌ PyMuPDF import failed: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("   ✅ python-dotenv: imported successfully")
    except ImportError as e:
        print(f"   ❌ python-dotenv import failed: {e}")
        return False

    return True

def test_backend_imports():
    """Test if backend modules can be imported"""
    print("🔧 Testing backend imports...")

    try:
        from backend import PDFProcessor, OpenRouterAPI, AdaptiveTestEngine
        print("   ✅ All backend classes imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Backend import failed: {e}")
        print("   Make sure backend.py is in the same directory")
        return False

def test_env_file():
    """Test environment file setup"""
    print("🔑 Testing environment setup...")

    if not os.path.exists(".env"):
        print("   ⚠️  .env file not found")
        print("   Create .env file with your OpenRouter API key")
        return False

    load_dotenv()
    api_key = os.getenv('OR_API_KEY')

    if not api_key:
        print("   ❌ OR_API_KEY not found in .env file")
        return False

    if api_key == "your_openrouter_api_key_here":
        print("   ⚠️  Please replace the placeholder API key with your actual key")
        return False

    if len(api_key) < 20:
        print("   ⚠️  API key seems too short, please verify it's correct")
        return False

    print("   ✅ API key found and appears valid")
    return True

def test_api_connection():
    """Test API connection"""
    print("🌐 Testing API connection...")

    try:
        from backend import OpenRouterAPI
        api = OpenRouterAPI()
        print("   ✅ OpenRouterAPI initialized successfully")
        return True
    except Exception as e:
        print(f"   ❌ API connection failed: {e}")
        return False

def test_file_structure():
    """Test if all required files are present"""
    print("📁 Testing file structure...")

    required_files = [
        "app.py",
        "backend.py", 
        "requirements.txt"
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            missing_files.append(file)

    if missing_files:
        print(f"   Missing files: {missing_files}")
        return False

    return True

def main():
    """Run all tests"""
    print("🧠 AI-Driven Adaptive Testing Platform - System Test")
    print("=" * 60)

    all_passed = True

    # Test file structure
    all_passed &= test_file_structure()
    print()

    # Test imports
    all_passed &= test_imports()
    print()

    # Test backend
    all_passed &= test_backend_imports()
    print()

    # Test environment
    all_passed &= test_env_file()
    print()

    # Test API connection
    all_passed &= test_api_connection()
    print()

    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the application.")
        print("\n🚀 To start the app, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above before running the app.")
        print("\n💡 Common solutions:")
        print("   - Run: pip install -r requirements.txt")
        print("   - Create .env file with your OpenRouter API key")
        print("   - Make sure all files are in the same directory")

    return all_passed

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
