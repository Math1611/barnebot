from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Listado de Modelos Disponibles ---")
for m in client.models.list():
    if 'embedContent' in m.supported_methods:
        print(f"✅ EMBEDDING: {m.name} (ID: {m.name.split('/')[-1]})")
    if 'generateContent' in m.supported_methods:
        print(f"🤖 GENERACIÓN: {m.name} (ID: {m.name.split('/')[-1]})")