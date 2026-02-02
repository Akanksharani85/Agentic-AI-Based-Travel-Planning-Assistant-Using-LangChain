import google.generativeai as genai
import os

# Yahan apni API Key daal
api_key = "AIzaSyBFQvq7VVxWTqMT072TSGuhFzylC61dLjU"

genai.configure(api_key=api_key)

print("🔍 Checking available models for your API Key...\n")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
            count += 1
    
    if count == 0:
        print("❌ Koi Model nahi mila! Shayad API Key galat hai ya permissions missing hain.")
    else:
        print("\n🎉 Badhai ho! Key kaam kar rahi hai.")

except Exception as e:
    print(f"❌ Error aaya: {e}")