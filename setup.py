import os
import subprocess
import sys

# 1. Configurações
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_NAME = "venv"
FOLDERS_TO_CREATE = [
    "data/docs",
    "src/core",
    "src"
]
REQUIREMENTS_CONTENT = """
langchain
openai
pypdf
unstructured
chromadb
python-dotenv
fastapi
uvicorn
"""
GITIGNORE_CONTENT = """
# Python
__pycache__/
*.pyc

# Virtual Environment
/venv/
.env

# Data
*.ipynb_checkpoints
"""

def create_venv():
    """Cria e ativa o ambiente virtual (venv)."""
    print(f"Criação do ambiente virtual '{VENV_NAME}'...")
    try:
        subprocess.run([sys.executable, "-m", "venv", VENV_NAME], check=True)
        print(f"Ambiente virtual criado em ./{VENV_NAME}")

        # Se estiver no Windows, a sintaxe de ativação é diferente.
        # Não ativaremos via script, apenas criaremos e instruiremos o usuário.
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar o ambiente virtual: {e}")
        sys.exit(1)

def create_folders():
    """Cria a estrutura de pastas do projeto."""
    print("Criação da estrutura de pastas...")
    for folder in FOLDERS_TO_CREATE:
        path = os.path.join(PROJECT_ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f" - Pasta criada: {folder}")

def create_initial_files():
    """Cria arquivos essenciais (.env, requirements.txt, .gitignore)."""
    print("Criação de arquivos essenciais...")
    
    # requirements.txt
    with open(os.path.join(PROJECT_ROOT, "requirements.txt"), "w") as f:
        f.write(REQUIREMENTS_CONTENT.strip())
    print(" - requirements.txt criado.")

    # .env
    with open(os.path.join(PROJECT_ROOT, ".env"), "w") as f:
        f.write("# OPENAI_API_KEY='SUA_CHAVE_AQUI'")
    print(" - .env criado (Adicione sua chave API aqui!).")

    # .gitignore
    with open(os.path.join(PROJECT_ROOT, ".gitignore"), "w") as f:
        f.write(GITIGNORE_CONTENT.strip())
    print(" - .gitignore criado.")
    
    # README.md
    with open(os.path.join(PROJECT_ROOT, "README.md"), "w") as f:
        f.write("# RAG Chatbot Agent")
    print(" - README.md criado.")


if __name__ == "__main__":
    print("--- INICIANDO SETUP DO PROJETO RAG CHATBOT ---")
    
    # 1. Cria o ambiente virtual
    create_venv()
    
    # 2. Cria a estrutura de pastas e arquivos
    create_folders()
    create_initial_files()
    
    print("\n--- SETUP CONCLUÍDO! ---")
    print("\nPRÓXIMOS PASSOS:")
    print(f"1. Ative o ambiente virtual: source {VENV_NAME}/bin/activate (ou .\\{VENV_NAME}\\Scripts\\activate no Windows).")
    print(f"2. Instale as dependências: pip install -r requirements.txt")
    print("3. Edite o arquivo .env e adicione sua OPENAI_API_KEY.")