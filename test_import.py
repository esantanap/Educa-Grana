# test_import.py
import sys
from pathlib import Path

# Adicionar src ao path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

print(f"📂 Diretório src: {src_dir}")
print(f"📄 Agent existe: {(src_dir / 'agent.py').exists()}")

try:
    from agent import answer_question
    print("✅ Import do agent funcionou!")
    
    # Teste básico
    response = answer_question("teste")
    print("✅ Agent executou!")
except Exception as e:
    print(f"❌ Erro: {e}")