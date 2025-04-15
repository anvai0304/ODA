# test_gemini.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")  # <- ensure .env has this

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Tell me about the Olympic Games in 3 lines.")
print(response.text.strip())
