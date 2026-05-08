import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Get API key
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("❌ GROQ_API_KEY not found in .env file!")
    print("\nPlease add this to your .env file:")
    print("GROQ_API_KEY=your_api_key_here")
    exit()

print("\n✅ API Key found!\n")

# Create Groq client
client = Groq(api_key=API_KEY)

print("Testing Groq API connection...\n")

try:
    # Simple test call
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "user", "content": "Say 'Hello from CodeSense AI'"}
        ],
        max_tokens=50
    )
    
    print("✅ Groq API is working perfectly!\n")
    print(f"Response: {response.choices[0].message.content}\n")
    
    print("📋 Available Models for CodeSense AI:")
    print("1. mixtral-8x7b-32768 (Best for code - RECOMMENDED)")
    print("2. llama-3.3-70b-versatile (Most powerful)")
    print("3. llama-3.1-8b-instant (Fastest)")
    print("4. gemma2-9b-it (Good for general)")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nPossible issues:")
    print("1. API key is invalid")
    print("2. No internet connection")
    print("3. API key format wrong (should start with 'gsk_')")