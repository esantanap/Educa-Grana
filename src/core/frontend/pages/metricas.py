# src/core/frontend/pages/metricas.py - Exibição do Relatório de Telemetria
import streamlit as st
from pathlib import Path
import subprocess
import time
import sys

st.set_page_config(
    layout="wide", 
    page_title="Métricas - IAmiga", 
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #A6193C 0%, #8B1532 100%); 
            color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;'>
    <h1 style='margin: 0; font-size: 2rem;'>📊 Relatório de Telemetria - IAmiga</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Dashboard de Análise de Uso e Performance</p>
</div>
""", unsafe_allow_html=True)

# Caminho do relatório HTML
# De: src/core/frontend/pages/metricas.py -> raiz do projeto
# parent = pages, parent.parent = frontend, parent.parent.parent = core, parent.parent.parent.parent = src
# parent.parent.parent.parent.parent = raiz
html_path = Path(__file__).parent.parent.parent.parent.parent / "data" / "telemetry_report.html"

# Debug: mostrar caminho no sidebar (pode remover depois)
# st.sidebar.text(f"Caminho: {html_path}")
# st.sidebar.text(f"Existe: {html_path.exists()}")

# Controles
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

with col1:
    if st.button("🔄 Gerar Novo Relatório", type="primary", use_container_width=True):
        with st.spinner("📊 Gerando relatório de telemetria... (pode demorar alguns segundos)"):
            try:
                # Caminho correto: voltar à raiz do projeto
                base_dir = Path(__file__).parent.parent.parent.parent.parent
                scripts_dir = base_dir / "scripts"
                analyze_script = scripts_dir / "analyze_telemetry.py"
                
                result = subprocess.run(
                    [sys.executable, str(analyze_script)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(base_dir)
                )
                if result.returncode == 0:
                    st.success("✅ Relatório gerado e atualizado!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Erro ao gerar relatório")
                    with st.expander("Ver detalhes do erro"):
                        st.code(result.stderr)
            except Exception as e:
                st.error(f"❌ Erro: {e}")

with col2:
    if st.button("🔃 Recarregar", use_container_width=True):
        st.rerun()

with col3:
    # Botão para baixar/abrir o HTML
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.download_button(
            label="📄 Baixar HTML",
            data=html_content,
            file_name="telemetria_report.html",
            mime="text/html",
            use_container_width=True
        )
    else:
        st.button("📄 Baixar HTML", disabled=True, use_container_width=True)

with col4:
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)

with col5:
    if auto_refresh:
        refresh_interval = st.number_input("⏱️ Segundos:", 30, 600, 60, 30, label_visibility="collapsed")
    else:
        refresh_interval = 60

st.markdown("---")

# Tentar carregar e exibir o relatório HTML
try:
    if html_path.exists():
        # Informações do arquivo
        file_size = html_path.stat().st_size / 1024  # KB
        file_mtime = html_path.stat().st_mtime
        last_modified = time.ctime(file_mtime)
        
        # Calcular tempo desde última modificação
        import datetime
        now = datetime.datetime.now().timestamp()
        seconds_ago = int(now - file_mtime)
        
        if seconds_ago < 60:
            time_ago = f"{seconds_ago}s atrás"
        elif seconds_ago < 3600:
            time_ago = f"{seconds_ago // 60}min atrás"
        else:
            time_ago = f"{seconds_ago // 3600}h atrás"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📁 Arquivo", "telemetry_report.html")
        with col2:
            st.metric("💾 Tamanho", f"{file_size:.2f} KB")
        with col3:
            st.metric("🕐 Última Atualização", time_ago)
        with col4:
            # Indicador de frescor
            if seconds_ago < 300:  # 5 minutos
                st.success("🟢 Atualizado")
            elif seconds_ago < 1800:  # 30 minutos
                st.warning("🟡 Pode atualizar")
            else:
                st.error("🔴 Desatualizado")
        
        st.markdown("---")
        
        # Ler e exibir o HTML completo
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Exibir o HTML completo em tamanho maior para melhor visualização
        st.components.v1.html(html_content, height=4000, scrolling=True)
        
    else:
        st.warning("📝 Relatório de telemetria não encontrado")
        st.info(f"📍 Esperado em: `{html_path}`")
        
        st.markdown("""
        ### 🚀 Como gerar o relatório?
        
        **Opção 1 - Clique no botão acima:**
        - Clique em "🔄 Atualizar Relatório e Recarregar"
        
        **Opção 2 - Execute no terminal:**
        ```bash
        python scripts/analyze_telemetry.py
        ```
        
        **Opção 3 - Use o main.py:**
        ```bash
        python main.py analyze
        ```
        """)

except Exception as e:
    st.error(f"❌ Erro ao carregar relatório: {e}")
    st.exception(e)

# Auto-refresh (opcional)
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.85em; margin-top: 2rem;'>
    📊 <strong>Relatório de Telemetria IAmiga</strong> | 
    Gerado automaticamente a partir dos dados de uso
</p>
""", unsafe_allow_html=True)
