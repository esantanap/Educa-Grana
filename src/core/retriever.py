# src/core/retriever.py
"""
Inicializa o Vector Store (ChromaDB) e cria o Retriever para buscar contexto relevante.
Garante uso do mesmo modelo de embedding e suporta OPENAI_BASE_URL/CA via .env.
"""

import os
from pathlib import Path
from typing import Literal, Optional
from dotenv import load_dotenv

# Imports relativos ao pacote core
from .config import Config

# Tenta importar a nova versão do Chroma primeiro
try:
    from langchain_chroma import Chroma
    print("✅ Usando langchain_chroma.Chroma (versão atualizada)")
    CHROMA_IMPORT = "langchain_chroma"
except ImportError:
    try:
        # Fallback para versão depreciada
        from langchain_community.vectorstores import Chroma
        print("⚠️  Usando langchain_community.vectorstores.Chroma (depreciado)")
        print("   Instale a versão atual: pip install langchain-chroma")
        CHROMA_IMPORT = "langchain_community"
    except ImportError as e:
        print(f"❌ Erro na importação de dependências do Chroma: {e}")
        print("Instale: pip install langchain-chroma langchain-openai langchain-community chromadb")
        raise

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.vectorstores import VectorStoreRetriever
    print("✅ Dependências do Retriever carregadas com sucesso")
except ImportError as e:
    print(f"❌ Erro na importação de dependências do Retriever: {e}")
    print("Instale: pip install langchain-openai langchain-core")
    raise

# Carregar .env (prioriza caminho customizado)
env_path = getattr(Config, "ENV_PATH", None)
if env_path:
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(override=True)

# Configurações
BASE_DIR = getattr(Config, "BASE_DIR", Path(__file__).resolve().parents[2])
CHROMA_PATH = getattr(Config, "CHROMA_PATH", BASE_DIR / "chroma")
EMBEDDING_MODEL = getattr(Config, "EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_ENV_VAR = getattr(Config, "OPENAI_ENV_VAR", "OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

def _get_api_key() -> str:
    key = os.getenv(OPENAI_ENV_VAR)
    if not key:
        raise RuntimeError(f"Variável {OPENAI_ENV_VAR} não encontrada. Configure .env.")
    return key

def _validate_env() -> None:
    _ = _get_api_key()
    if not OPENAI_BASE_URL:
        print("ℹ️ OPENAI_BASE_URL não definido. Usando endpoint padrão.")
    ca = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("SSL_CERT_FILE")
    if not ca:
        print("ℹ️ CA PEM não definido (REQUESTS_CA_BUNDLE/SSL_CERT_FILE). Configure se usar proxy/CA interna.")

def get_chroma_db():
    """
    Carrega a instância persistente do ChromaDB com o mesmo modelo de embedding usado na indexação.
    """
    if not Path(CHROMA_PATH).exists():
        raise FileNotFoundError(
            f"❌ Banco de dados vetorial não encontrado em {CHROMA_PATH}. "
            "Execute a indexação primeiro: python -m src.core.embedding"
        )

    _validate_env()

    # Inicializa o Embedding (mesmo modelo e endpoint da indexação)
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_base=OPENAI_BASE_URL or None,
        openai_api_key=_get_api_key(),
    )

    # Carrega Chroma persistente
    print("🗄️ Carregando ChromaDB persistente...")
    db = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings,
        collection_name="IAmiga_docs",
    )
    return db

def get_context_retriever(
    k: int = 6,
    search_type: Literal["similarity", "mmr"] = "similarity",
    score_threshold: Optional[float] = None,
) -> VectorStoreRetriever:
    """
    Cria e retorna o LangChain Retriever a partir do ChromaDB.
    Args:
        k: Número de chunks mais relevantes a retornar (otimizado para 6).
        search_type: 'similarity' (padrão) ou 'mmr' (diversidade).
        score_threshold: se fornecido, filtra por score mínimo (suporte dependendo de versão).
    """
    db = get_chroma_db()

    search_kwargs = {"k": k}
    if score_threshold is not None:
        search_kwargs["score_threshold"] = score_threshold

    retriever = db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
    print(f"✅ Retriever inicializado (search_type='{search_type}', k={k}).")
    return retriever

# --- Função de teste ---
def main() -> None:
    """Teste do retriever."""
    print("=" * 60)
    print("🔍 TESTE DO RETRIEVER DE CONTEXTO")
    print("=" * 60)

    try:
        retriever = get_context_retriever(k=6)
    except Exception as e:
        print(f"❌ Falha ao inicializar retriever: {e}")
        return

    query = "Quais são os passos de inicialização do sistema após uma falha de energia?"
    print(f"\n[QUERY]: {query}")

    try:
        relevant_docs = retriever.invoke(query)
    except Exception as e:
        print(f"❌ Erro ao executar a busca: {e}")
        return

    print(f"\n-> Documentos relevantes encontrados ({len(relevant_docs)} chunks):")
    for i, doc in enumerate(relevant_docs):
        source = doc.metadata.get("source", "N/A")
        page = doc.metadata.get("page_number", "N/A")
        preview = (doc.page_content or "")[:200].replace("\n", " ")
        print(f"--- Chunk {i+1} (Fonte: {source}, Página: {page}) ---")
        print(f"{preview}...")
        print("-" * 60)

if __name__ == "__main__":
    main()