# scripts/langchain_llm_simple.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("OPENAI_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "bnb-gpt-5-mini")
VERIFY = os.getenv("SSL_VERIFY", "false").lower() != "false"

def call_llm(text):
    url = BASE_URL.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Responda em uma frase."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0,
        "max_tokens": 64
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=20, verify=VERIFY)
    print("Status:", resp.status_code)
    print("Body:", resp.text[:800])

if __name__ == "__main__":
    call_llm("Diga 'ok'.")
    call_llm("Qual a capital do Ceará?")
