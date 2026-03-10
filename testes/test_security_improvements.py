"""
Script de teste para verificar as melhorias de segurança implementadas
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_ssl_configuration():
    """Testa configuração SSL"""
    print("🔒 Testando configuração SSL...")
    
    # Verificar variáveis de ambiente
    cert_path = os.getenv('REQUESTS_CA_BUNDLE') or os.getenv('SSL_CERT_FILE')
    
    if cert_path:
        if os.path.exists(cert_path):
            print(f"✅ Certificado SSL encontrado: {cert_path}")
        else:
            print(f"⚠️ Certificado configurado mas não existe: {cert_path}")
    else:
        print("⚠️ Certificado SSL não configurado (usará certificados padrão do sistema)")
    
    return True

def test_env_variables():
    """Testa se variáveis de ambiente estão configuradas"""
    print("\n🔑 Testando variáveis de ambiente...")
    
    required_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL']
    optional_vars = ['REQUESTS_CA_BUNDLE', 'SSL_CERT_FILE']
    
    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mascarar API key
            if 'KEY' in var:
                masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"✅ {var}: {masked}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NÃO CONFIGURADO")
            all_ok = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"ℹ️  {var}: {value}")
    
    return all_ok

def test_agent_import():
    """Testa importação do agent"""
    print("\n📦 Testando importação do agent...")
    
    try:
        from agent import answer_question, configure_ssl_flexible
        print("✅ Agent importado com sucesso!")
        
        # Testar configuração SSL
        cert_result = configure_ssl_flexible()
        if cert_result:
            print(f"✅ SSL configurado: {cert_result}")
        else:
            print("ℹ️  SSL não configurado (usará padrão)")
        
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar agent: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_simple_question():
    """Testa uma pergunta simples"""
    print("\n❓ Testando pergunta simples...")
    
    try:
        from agent import answer_question
        
        question = "O que é o Crediamigo?"
        print(f"Pergunta: {question}")
        print("Processando...")
        
        response = answer_question(question)
        
        if response and len(response) > 50:
            print(f"✅ Resposta recebida ({len(response)} caracteres)")
            print(f"\nPrimeiros 200 caracteres:\n{response[:200]}...")
            return True
        else:
            print(f"⚠️ Resposta muito curta ou vazia: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar pergunta: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTE DAS MELHORIAS DE SEGURANÇA - IAMIGA")
    print("=" * 70)
    
    results = []
    
    # Teste 1: Variáveis de ambiente
    results.append(("Variáveis de ambiente", test_env_variables()))
    
    # Teste 2: SSL
    results.append(("Configuração SSL", test_ssl_configuration()))
    
    # Teste 3: Import
    results.append(("Importação do Agent", test_agent_import()))
    
    # Teste 4: Pergunta simples
    results.append(("Processamento de pergunta", test_simple_question()))
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam")
        return 1

if __name__ == "__main__":
    exit(main())
