# src/core/frontend/pages/logs.py - Página de Logs para Gestores
import streamlit as st
from pathlib import Path
import time

st.set_page_config(
    layout="wide", 
    page_title="Logs do Sistema - IAmiga", 
    page_icon="📋",
    initial_sidebar_state="collapsed"
)

# === PÁGINA DE LOGS ===

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #A6193C 0%, #8B1532 100%); 
            color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;'>
    <h1 style='margin: 0; font-size: 2rem;'>📋 Logs do Sistema - IAmiga</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Monitoramento em Tempo Real - Área de Gestão</p>
</div>
""", unsafe_allow_html=True)

# Controles
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    num_lines = st.slider("📊 Número de linhas:", 10, 500, 100, 10)

with col2:
    auto_refresh = st.checkbox("🔄 Auto-atualizar", value=False)

with col3:
    refresh_interval = st.number_input("⏱️ Intervalo (s):", 1, 60, 5, 1)

with col4:
    if st.button("🔄 Atualizar Agora", type="primary"):
        st.rerun()

# Placeholder para auto-refresh
if auto_refresh:
    st.info(f"🔄 Auto-atualização ativa (a cada {refresh_interval}s)")

# Leitura e exibição dos logs
st.markdown("---")

try:
    log_path = Path(__file__).parent.parent.parent.parent.parent / "data" / "app.log"
    
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            total_lines = len(lines)
            last_lines = lines[-num_lines:] if total_lines > num_lines else lines
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Total de Linhas", total_lines)
        with col2:
            st.metric("👁️ Exibindo", len(last_lines))
        with col3:
            info_count = sum(1 for line in last_lines if "INFO" in line)
            st.metric("ℹ️ INFO", info_count)
        with col4:
            error_count = sum(1 for line in last_lines if "ERROR" in line or "WARNING" in line)
            st.metric("⚠️ WARN/ERROR", error_count)
        
        st.markdown("---")
        
        # Filtros
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_text = st.text_input("🔍 Filtrar logs (texto):", placeholder="Digite para filtrar...")
        with col2:
            log_level = st.selectbox("📊 Nível:", ["TODOS", "INFO", "WARNING", "ERROR"])
        
        # Aplicar filtros
        filtered_lines = last_lines
        if filter_text:
            filtered_lines = [line for line in filtered_lines if filter_text.lower() in line.lower()]
        if log_level != "TODOS":
            filtered_lines = [line for line in filtered_lines if log_level in line]
        
        # Exibir logs
        st.markdown("### 📜 Logs")
        if filtered_lines:
            logs_text = "".join(filtered_lines)
            st.code(logs_text, language="log", line_numbers=True)
            st.caption(f"📊 Mostrando {len(filtered_lines)} de {len(last_lines)} linhas (Total: {total_lines})")
        else:
            st.warning("🔍 Nenhum log encontrado com os filtros aplicados")
        
        # Informações do arquivo
        st.markdown("---")
        file_size = log_path.stat().st_size / 1024  # KB
        last_modified = time.ctime(log_path.stat().st_mtime)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📁 Arquivo: `{log_path}`")
        with col2:
            st.info(f"💾 Tamanho: {file_size:.2f} KB | 🕐 Modificado: {last_modified}")
        
    else:
        st.warning("📝 Nenhum arquivo de log disponível ainda")
        st.info(f"📍 Esperado em: `{log_path}`")

except Exception as e:
    st.error(f"❌ Erro ao ler logs: {e}")
    st.exception(e)

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# Footer
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.85em; margin-top: 2rem;'>
    📋 <strong>Logs do Sistema IAmiga</strong> | 
    👥 Área de Gestão
</p>
""", unsafe_allow_html=True)
