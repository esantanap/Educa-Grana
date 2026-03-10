# fix_ssl_agent.py - Script para corrigir SSL no agent
import os

def create_ssl_fix():
    """Criar função de correção SSL"""
    ssl_fix_code = '''# Correção SSL para certificados corporativos
import ssl
import urllib3
import os

def configure_ssl():
    """Configurar SSL para usar certificados corporativos"""
    cert_path = r"C:\Users\F147176\certs\ca-bnb.pem"
    
    if os.path.exists(cert_path):
        # Configurar para requests
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['CURL_CA_BUNDLE'] = cert_path
        os.environ['SSL_CERT_FILE'] = cert_path
        
        print(f"✅ Certificados configurados: {cert_path}")
        return cert_path
    else:
        print("⚠️ Certificado não encontrado, usando verificação padrão")
        return True

# Chamar configuração SSL
configure_ssl()

'''
    return ssl_fix_code

def apply_ssl_fix():
    """Aplicar correção SSL no arquivo agent"""
    
    # Caminho dos arquivos
    source_file = "src/core/agent_semantic_hybrid.py"
    target_file = "src/agent_semantic_fixed.py"
    
    # Verificar se arquivo fonte existe
    if not os.path.exists(source_file):
        print(f"❌ Arquivo não encontrado: {source_file}")
        return False
    
    try:
        # Ler arquivo original
        with open(source_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Criar correção SSL
        ssl_fix = create_ssl_fix()
        
        # Combinar correção + conteúdo original
        updated_content = ssl_fix + "\n\n" + original_content
        
        # Salvar arquivo corrigido
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Versão corrigida criada: {target_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aplicar correção: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Aplicando correção SSL no agent...")
    print("=" * 50)
    
    if apply_ssl_fix():
        print("\n🎉 Correção aplicada com sucesso!")
        print("📝 Execute: python src/agent_semantic_fixed.py")
    else:
        print("\n❌ Falha na aplicação da correção")