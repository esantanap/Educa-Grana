# src/core/test_azure_connection.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_azure_openai_connection():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "bnb-gpt-5.1-mini")

    print("🔍 Testando conexão com Azure OpenAI do BNB...")
    print("=" * 50)
    print(f"🔑 API Key: {'✅ Presente' if api_key else '❌ Ausente'}")
    print(f"🔗 Base URL: {base_url}")
    print(f"🤖 Modelo: {model}")
    print()

    if not api_key or not base_url:
        print("❌ Configuração incompleta")
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "IAmiga-RAG/1.0"
    }

    # Teste 1: (opcional) tentar listar modelos, mas não falhar se não existir
    print("🧪 Teste 1: Verificando endpoint de modelos (se existir)...")
    try:
        models_url = f"{base_url}/models"
        response = requests.get(models_url, headers=headers, timeout=30)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            try:
                models_data = response.json()
                print(f"✅ Endpoint de modelos acessível")
                print(f"📋 Modelos encontrados: {len(models_data.get('data', []))}")
            except:
                print("⚠️ Resposta não é JSON válido")
        elif response.status_code == 404:
            print("ℹ️ Endpoint /models não disponível neste serviço, seguindo para o chat.")
        else:
            print(f"ℹ️ Resposta inesperada para /models: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Erro ao consultar /models: {e}")

    print()

    # Teste 2: Chat completion
    print("🧪 Teste 2: Chat completion...")
    try:
        chat_url = f"{base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Responda apenas 'OK' se estiver funcionando"}
            ],
            "max_tokens": 10,
            "temperature": 0
        }

        response = requests.post(chat_url, json=payload, headers=headers, timeout=30)

        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                message = data['choices'][0]['message']['content']
                print(f"✅ Resposta: {message}")
                print("=" * 50)
                print("🎯 Resultado: ✅ SUCESSO")
                return True
            except Exception as e:
                print(f"⚠️ Erro ao processar resposta: {e}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📄 Resposta: {response.text[:500]}")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

    print("=" * 50)
    print("🎯 Resultado: ❌ FALHA")
    return False

if __name__ == "__main__":
    test_azure_openai_connection()
