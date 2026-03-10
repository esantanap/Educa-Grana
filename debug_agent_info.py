# debug_agent_info.py
import os
import sys

def check_agent_info():
    print("🔍 DIAGNÓSTICO DO AGENT")
    print("=" * 50)
    
    # Verificar diretório atual
    print(f"📁 Diretório atual: {os.getcwd()}")
    
    # Verificar arquivos agent disponíveis
    print("\n📄 Arquivos agent encontrados:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if "agent" in file.lower() and file.endswith(".py"):
                full_path = os.path.join(root, file)
                size = os.path.getsize(full_path)
                print(f"  📄 {full_path} ({size} bytes)")
    
    # Verificar qual agent está sendo importado
    print(f"\n🐍 Python path: {sys.path}")
    
    # Tentar importar agent
    sys.path.append('src')
    try:
        import agent
        agent_file = agent.__file__ if hasattr(agent, '__file__') else "Não encontrado"
        print(f"✅ Agent importado de: {agent_file}")
        
        # Verificar funções disponíveis
        functions = [f for f in dir(agent) if not f.startswith('_')]
        print(f"📋 Funções disponíveis: {functions}")
        
        # Verificar se tem busca semântica
        if hasattr(agent, 'LocalSemanticSearchEngine'):
            print("✅ LocalSemanticSearchEngine encontrada")
        else:
            print("❌ LocalSemanticSearchEngine NÃO encontrada")
            
        if hasattr(agent, 'search_knowledge_semantic'):
            print("✅ search_knowledge_semantic encontrada")
        else:
            print("❌ search_knowledge_semantic NÃO encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao importar agent: {e}")

if __name__ == "__main__":
    check_agent_info()