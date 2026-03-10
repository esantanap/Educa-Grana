# scripts/test_embeddings.py
import os
import traceback
from dotenv import load_dotenv

def main():
    # carrega .env
    load_dotenv(override=True)

    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    api_key_env = os.getenv("OPENAI_ENV_VAR", "OPENAI_API_KEY")
    api_key = os.getenv(api_key_env)
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip()
    ca = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("SSL_CERT_FILE")

    print("=== Diagnóstico de Embeddings ===")
    print(f"BASE_URL: {base_url or '(DEFAULT)'}")
    print(f"EMBEDDING_MODEL: {model}")
    print(f"API KEY presente?: {'SIM' if bool(api_key) else 'NÃO'}")
    print(f"CA PEM: {ca or '(NONE)'}")

    # validações básicas
    if not api_key:
        print(f"ERRO: Variável de ambiente '{api_key_env}' não encontrada.")
        return

    try:
        from langchain_openai import OpenAIEmbeddings
    except Exception as e:
        print(f"Import de langchain_openai falhou: {e}")
        print("Instale: pip install langchain-openai")
        return

    try:
        emb = OpenAIEmbeddings(
            model=model,
            openai_api_base=base_url or None,
            openai_api_key=api_key,
        )
        # chamada de teste
        vec = emb.embed_query("ping de conectividade")
        print(f"OK: chamada de embeddings retornou vetor com {len(vec)} dimensões")
    except Exception as e:
        print("FALHA na chamada de embeddings:")
        print(f"- Erro: {e}")
        traceback.print_exc()
        print("Dicas:")
        print("  • Se o erro for 401: verifique token e formato de auth aceito pelo endpoint")
        print("  • Se for 404: ajuste OPENAI_BASE_URL para a rota correta (geralmente termina com /embeddings)")
        print("  • Se for SSL: valide REQUESTS_CA_BUNDLE/SSL_CERT_FILE apontando para o PEM correto")
        print("  • Se for 400: confira se o modelo está habilitado no serviço")

if __name__ == "__main__":
    main()
