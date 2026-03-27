#!/usr/bin/env python3
"""
Generate secure Flask secret key for production
Usage: python3 generate_secret_key.py
"""
import secrets
import os

def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    return secrets.token_hex(32)

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print(f"\n🔐 Your secure Flask secret key:\n")
    print(f"   {secret_key}\n")
    print(f"Copy this to your Render environment variables as FLASK_SECRET_KEY\n")
    print(f"Or add to .env.production file\n")
