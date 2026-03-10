# scripts/check_imports.py
import importlib
import sys
import traceback
from types import ModuleType

# Símbolos críticos que seu projeto usa
CHECKS = [
    # Loaders e documentos
    {
        "name": "DirectoryLoader (langchain_community)",
        "module": "langchain_community.document_loaders",
        "symbol": "DirectoryLoader",
    },
    {
        "name": "UnstructuredFileLoader (langchain_community)",
        "module": "langchain_community.document_loaders",
        "symbol": "UnstructuredFileLoader",
    },
    {
        "name": "RecursiveCharacterTextSplitter (langchain-text-splitters)",
        "module": "langchain_text_splitters",
        "symbol": "RecursiveCharacterTextSplitter",
    },
    {
        "name": "Document (langchain_core.documents)",
        "module": "langchain_core.documents",
        "symbol": "Document",
    },

    # Vector store & retriever
    {
        "name": "Chroma (langchain_community.vectorstores)",
        "module": "langchain_community.vectorstores",
        "symbol": "Chroma",
    },
    {
        "name": "VectorStoreRetriever (langchain_core.vectorstores)",
        "module": "langchain_core.vectorstores",
        "symbol": "VectorStoreRetriever",
    },

    # Core do LangChain (prompts, parsing, runnables)
    {
        "name": "ChatPromptTemplate (langchain_core.prompts)",
        "module": "langchain_core.prompts",
        "symbol": "ChatPromptTemplate",
    },
    {
        "name": "StrOutputParser (langchain_core.output_parsers)",
        "module": "langchain_core.output_parsers",
        "symbol": "StrOutputParser",
    },
    {
        "name": "RunnablePassthrough (langchain_core.runnables)",
        "module": "langchain_core.runnables",
        "symbol": "RunnablePassthrough",
    },
    {
        "name": "RunnableLambda (langchain_core.runnables)",
        "module": "langchain_core.runnables",
        "symbol": "RunnableLambda",
    },

    # OpenAI via LangChain
    {
        "name": "ChatOpenAI (langchain_openai)",
        "module": "langchain_openai",
        "symbol": "ChatOpenAI",
    },
    {
        "name": "OpenAIEmbeddings (langchain_openai)",
        "module": "langchain_openai",
        "symbol": "OpenAIEmbeddings",
    },
]

TOP_LEVEL_MODULES = [
    "langchain_core",
    "langchain_openai",
    "langchain_community",
    "langchain_text_splitters",
    "openai",
    "chromadb",
    "dotenv",
    "unstructured",
    "pypdf",
    "streamlit",
]

# Mapeamento pacote → nome de distribuição para consulta de versão
DIST_NAMES = {
    "langchain_core": "langchain-core",
    "langchain_openai": "langchain-openai",
    "langchain_community": "langchain-community",
    "langchain_text_splitters": "langchain-text-splitters",
    "openai": "openai",
    "chromadb": "chromadb",
    "dotenv": "python-dotenv",
    "unstructured": "unstructured",
    "pypdf": "pypdf",
    "streamlit": "streamlit",
}


def try_import(module_name: str) -> ModuleType | None:
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def check_symbol(module_name: str, symbol: str):
    m = try_import(module_name)
    if m is None:
        return (False, f"module '{module_name}' not found")
    if not hasattr(m, symbol):
        available = dir(m)
        return (False, f"symbol '{symbol}' not in module {module_name}; available: {available[:20]}{'...' if len(available)>20 else ''}")
    obj = getattr(m, symbol)
    origin = getattr(obj, "__module__", getattr(obj, "__class__", type(obj)).__module__)
    source = getattr(m, "__file__", "built-in or namespace package")
    return (True, f"OK — from {module_name} (file: {source}; symbol origin: {origin})")


def show_versions():
    print("\nPackage versions (importlib.metadata):")
    # usar importlib.metadata nativo ou backport
    try:
        from importlib.metadata import version, PackageNotFoundError
    except Exception:
        try:
            from importlib_metadata import version, PackageNotFoundError  # type: ignore
        except Exception:
            print("  importlib.metadata not available")
            return

    for mod, dist in DIST_NAMES.items():
        try:
            v = version(dist)
            print(f"  - {dist}: {v}")
        except PackageNotFoundError:
            print(f"  - {dist}: NOT INSTALLED")


def main():
    print("Python executable:", sys.executable)
    print("sys.path sample (first 10):")
    for p in sys.path[:10]:
        print("  ", p)

    print("\nRunning symbol checks:\n")
    for c in CHECKS:
        ok, msg = check_symbol(c["module"], c["symbol"])
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {c['name']}: {msg}")

    print("\nTop-level module presence:")
    for mod in TOP_LEVEL_MODULES:
        m = try_import(mod)
        if m is None:
            print(f"  - {mod}: NOT FOUND")
        else:
            print(f"  - {mod}: FOUND (file: {getattr(m,'__file__', 'pkg')})")

    show_versions()

    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Unexpected error during checks:")
        traceback.print_exc()
