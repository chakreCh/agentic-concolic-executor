import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load the safe .env file
load_dotenv()

# 2. Get the key securely
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

    print("Checking available models for your API key...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"FOUND: {m.name}")
    except Exception as e:
        print(f"Error: {e}")