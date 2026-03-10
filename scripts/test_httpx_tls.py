# scripts/test_httpx_tls.py
import os
from dotenv import load_dotenv
import httpx

load_dotenv(override=True)
url = os.getenv("OPENAI_BASE_URL")
ca = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("SSL_CERT_FILE")

print("URL:", url)
print("CA:", ca)

try:
    with httpx.Client(verify=ca) as client:
        r = client.get(url, timeout=10)
        print("Status:", r.status_code)
except Exception as e:
    print("Erro httpx:", e)

