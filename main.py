"""
main.py - Sistema IAmiga Modular
Orquestrador principal que gerencia os diferentes módulos do sistema
"""
import sys
import argparse
from pathlib import Path

def main():
    """Função principal que orquestra o sistema"""
    parser = argparse.ArgumentParser(description='IAmiga - Sistema RAG Modular')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: Iniciar todos os servidores
    start_parser = subparsers.add_parser('start', help='Iniciar todos os servidores (Web, Logs, Métricas)')
    
    # Comando: Interface Web (Streamlit)
    web_parser = subparsers.add_parser('web', help='Iniciar interface web (Streamlit)')
    web_parser.add_argument('--host', default='0.0.0.0', help='Host (padrão: 0.0.0.0)')
    web_parser.add_argument('--port', type=int, default=8501, help='Porta (padrão: 8501)')
    
    # Comando: Processar documentos
    process_parser = subparsers.add_parser('process', help='Processar documentos e criar base de conhecimento')
    
    # Comando: Análise de telemetria
    analyze_parser = subparsers.add_parser('analyze', help='Gerar relatório de telemetria')
    
    # Comando: Servidor de logs
    logs_parser = subparsers.add_parser('logs', help='Servidor de visualização de logs')
    logs_parser.add_argument('--port', type=int, default=8502, help='Porta (padrão: 8502)')
    
    # Comando: Servidor de métricas
    metrics_parser = subparsers.add_parser('metrics', help='Servidor de visualização de métricas')
    metrics_parser.add_argument('--port', type=int, default=8503, help='Porta (padrão: 8503)')
    
    # Comando: Servidor de explicabilidade (XAI)
    xai_parser = subparsers.add_parser('xai', help='Servidor de explicabilidade (XAI)')
    xai_parser.add_argument('--port', type=int, default=8504, help='Porta (padrão: 8504)')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        start_all_servers()
    elif args.command == 'web':
        start_web_interface(args.host, args.port)
    elif args.command == 'process':
        process_documents()
    elif args.command == 'analyze':
        analyze_telemetry()
    elif args.command == 'logs':
        start_logs_server(args.port)
    elif args.command == 'metrics':
        start_metrics_server(args.port)
    elif args.command == 'xai':
        start_xai_server(args.port)
    else:
        parser.print_help()

def start_all_servers():
    """Iniciar todos os servidores simultaneamente"""
    import subprocess
    import time
    import webbrowser
    
    print("=" * 70)
    print("🚀 INICIANDO TODOS OS SERVIDORES IAMIGA")
    print("=" * 70)
    
    base_path = Path(__file__).parent / "src" / "core" / "frontend"
    
    servers = [
        {
            'name': 'Web Interface',
            'file': base_path / "app.py",
            'port': 8501,
            'url': 'http://localhost:8501',
            'emoji': '🌐'
        },
        {
            'name': 'Logs',
            'file': base_path / "pages" / "logs.py",
            'port': 8502,
            'url': 'http://localhost:8502',
            'emoji': '📋'
        },
        {
            'name': 'Métricas',
            'file': base_path / "pages" / "metricas.py",
            'port': 8503,
            'url': 'http://localhost:8503',
            'emoji': '📊'
        },
        {
            'name': 'Explicabilidade (XAI)',
            'file': base_path / "pages" / "explicabilidade.py",
            'port': 8504,
            'url': 'http://localhost:8504',
            'emoji': '🔍'
        }
    ]
    
    processes = []
    
    for server in servers:
        print(f"\n{server['emoji']} Iniciando {server['name']}...")
        print(f"   Porta: {server['port']}")
        print(f"   URL: {server['url']}")
        
        cmd = [
            "streamlit", "run", str(server['file']),
            "--server.address", "0.0.0.0",
            "--server.port", str(server['port']),
            "--server.headless", "true"
        ]
        
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        processes.append({'name': server['name'], 'process': proc, 'url': server['url']})
        time.sleep(2)  # Aguardar servidor iniciar
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS SERVIDORES INICIADOS COM SUCESSO!")
    print("=" * 70)
    print("\n📍 URLs de Acesso:")
    for server in servers:
        print(f"   {server['emoji']} {server['name']}: {server['url']}")
    
    print("\n🌐 Abrindo navegadores...")
    time.sleep(3)
    
    # Abrir navegadores automaticamente
    for server in servers:
        try:
            webbrowser.open(server['url'])
            time.sleep(1)
        except:
            pass
    
    print("\n" + "=" * 70)
    print("⚠️  Pressione Ctrl+C para parar todos os servidores")
    print("=" * 70)
    
    try:
        # Manter script rodando
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Parando todos os servidores...")
        for proc_info in processes:
            try:
                proc_info['process'].terminate()
                print(f"   ✓ {proc_info['name']} parado")
            except:
                pass
        print("\n✅ Todos os servidores foram parados.")


def start_web_interface(host: str, port: int):
    """Iniciar interface web Streamlit"""
    import subprocess
    import os
    
    app_path = Path(__file__).parent / "src" / "core" / "frontend" / "app.py"
    
    print(f"🚀 Iniciando IAmiga Web Interface em http://{host}:{port}")
    print(f"📁 Arquivo: {app_path}")
    
    cmd = [
        "streamlit", "run", str(app_path),
        "--server.address", host,
        "--server.port", str(port)
    ]
    
    subprocess.run(cmd)

def process_documents():
    """Processar documentos e criar base de conhecimento"""
    import subprocess
    
    script_path = Path(__file__).parent / "src" / "create_vectordb.py"
    
    print("📚 Processando documentos...")
    print(f"📁 Script: {script_path}")
    
    subprocess.run(["python", str(script_path)])

def analyze_telemetry():
    """Gerar relatório de telemetria"""
    import subprocess
    
    script_path = Path(__file__).parent / "scripts" / "analyze_telemetry.py"
    
    print("📊 Gerando relatório de telemetria...")
    print(f"📁 Script: {script_path}")
    
    subprocess.run(["python", str(script_path)])

def start_logs_server(port: int):
    """Iniciar servidor dedicado de logs"""
    import subprocess
    
    logs_app = Path(__file__).parent / "src" / "core" / "frontend" / "pages" / "logs.py"
    
    print(f"📋 Iniciando servidor de logs em http://localhost:{port}")
    print(f"📁 Arquivo: {logs_app}")
    
    cmd = [
        "streamlit", "run", str(logs_app),
        "--server.address", "0.0.0.0",
        "--server.port", str(port)
    ]
    
    subprocess.run(cmd)

def start_metrics_server(port: int):
    """Iniciar servidor dedicado de métricas"""
    import subprocess
    
    print("=" * 70)
    print("📊 SERVIDOR DE MÉTRICAS")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    metrics_app = base_dir / "src" / "core" / "frontend" / "pages" / "metricas.py"
    
    url = f"http://localhost:{port}"
    print(f"📍 URL: {url}")
    print(f"📁 Arquivo: {metrics_app}")
    print("=" * 70)
    
    # Abrir navegador após alguns segundos
    import webbrowser
    import threading
    
    def open_browser():
        time.sleep(3)  # Aguardar servidor iniciar
        try:
            webbrowser.open(url)
            print(f"\n🌐 Navegador aberto: {url}")
        except:
            print(f"\n⚠️ Não foi possível abrir navegador automaticamente")
            print(f"   Acesse manualmente: {url}")
    
    # Abrir navegador em thread separada
    threading.Thread(target=open_browser, daemon=True).start()
    
    cmd = [
        "streamlit", "run", str(metrics_app),
        "--server.address", "0.0.0.0",
        "--server.port", str(port)
    ]
    
    subprocess.run(cmd, cwd=str(base_dir))

def start_xai_server(port: int):
    """Iniciar servidor dedicado de explicabilidade (XAI)"""
    import subprocess
    import webbrowser
    import threading
    import time
    
    print("=" * 70)
    print("🔍 SERVIDOR DE EXPLICABILIDADE (XAI)")
    print("=" * 70)
    
    base_dir = Path(__file__).parent
    xai_app = base_dir / "src" / "core" / "frontend" / "pages" / "explicabilidade.py"
    
    url = f"http://localhost:{port}"
    print(f"📍 URL: {url}")
    print(f"📁 Arquivo: {xai_app}")
    print("=" * 70)
    
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open(url)
            print(f"\n🌐 Navegador aberto: {url}")
        except:
            print(f"\n⚠️ Não foi possível abrir navegador automaticamente")
            print(f"   Acesse manualmente: {url}")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    cmd = [
        "streamlit", "run", str(xai_app),
        "--server.address", "0.0.0.0",
        "--server.port", str(port)
    ]
    
    subprocess.run(cmd, cwd=str(base_dir))

if __name__ == "__main__":
    main()
