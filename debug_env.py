#!/usr/bin/env python3
"""Test script to debug environment variables"""
import sys
import os
from dotenv import load_dotenv

# Print current directory
print(f"Current directory: {os.getcwd()}")

# Check .env file location
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Looking for .env file at: {env_path}")
print(f".env file exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    print("\n.env file content:")
    with open(env_path, 'r', encoding='utf-8') as f:
        print(f.read())

# Load .env
load_dotenv(env_path)
print("\nEnvironment variables after load_dotenv:")
print(f"DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY')}")
print(f"QWEN_MODEL: {os.getenv('QWEN_MODEL')}")

# Try to import ai_analyzer
print("\nTrying to import ai_analyzer:")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from modules.ai_analyzer import AIAnalyzer
    ai = AIAnalyzer()
    print(f"AI enabled: {ai.enabled}")
    print(f"AI has client: {hasattr(ai, 'client')}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
