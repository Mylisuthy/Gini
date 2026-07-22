import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from src.core.config_manager import config

api_key = config.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Modelos de embedding disponibles:")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(m.name)
