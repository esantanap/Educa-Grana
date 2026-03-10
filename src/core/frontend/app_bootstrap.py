# src/core/frontend/app_bootstrap.py - VERSÃO BOOTSTRAP COM LAYOUT MODERNO
import streamlit as st
import sys
from pathlib import Path
import base64
import logging
import json

# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide", page_title="IAmiga - Assistente RAG", page_icon="🤖")

def get_image_base64(image_path: Path) -> str:
    """Converter imagem para base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.warning(f"Erro ao carregar imagem: {e}")
        return ""

def log_vote(question: str, vote: str, doc_ids: list):
    """Registrar voto do usuário (thumbs up/down) em telemetria"""
    try:
        telemetry_path = Path(__file__).parent.parent.parent.parent / "data" / "telemetry.log"
        with open(telemetry_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "event": "vote", 
                "q": question, 
                "vote": vote, 
                "doc_ids": doc_ids
            }) + "\n")
        logger.info(f"[VOTE] {vote} para pergunta: {question[:50]}...")
    except Exception as e:
        logger.warning(f"[VOTE] Erro ao gravar voto: {e}")

# Configurar path para importar o agent
app_file = Path(__file__)
src_dir = app_file.parent.parent.parent

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Importar agent
try:
    from agent import answer_question
    logger.info("[APP] Agent importado com sucesso!")
except ImportError as e:
    st.error(f"❌ Erro ao importar agent: {e}")
    logger.error(f"[APP] Erro de importação: {e}")
    st.stop()

# CSS Bootstrap + Custom
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    /* Reset Streamlit */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
    
    /* Header */
    .custom-header {
        background: linear-gradient(135deg, #A6193C 0%, #8B1532 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .custom-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .custom-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }
    
    /* Chat Container */
    .chat-container {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 1rem;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Mensagens */
    .user-msg {
        background: linear-gradient(135deg, #e8e8e8 0%, #d4d4d4 100%);
        padding: 0.75rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 15%;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .assistant-msg {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 15%;
        border-left: 4px solid #A6193C;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-msg strong {
        color: #646464;
    }
    
    .assistant-msg strong {
        color: #A6193C;
    }
    
    /* Input area */
    .input-area {
        background: white;
        padding: 1rem;
        border-top: 2px solid #dee2e6;
        border-radius: 10px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    
    /* Scrollbar personalizada */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Botões */
    .stButton button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado
if "messages" not in st.session_state:
    st.session_state.messages = []
if "votes" not in st.session_state:
    st.session_state.votes = {}

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Status do Sistema")
    st.success("✅ Agent RAG Operacional")
    st.success("✅ Busca Semântica Ativa")
    st.success("✅ Base: 1.035 documentos")
    
    st.markdown("---")
    st.markdown("### 💡 Perguntas Sugeridas")
    st.info("""
    - O que é o Educa Grana?
    - Quais linhas de crédito?
    - Como solicitar crédito?
    - O que é Educa Grana Delas?
    - Documentos necessários?
    """)
    
    st.markdown("---")
    if st.session_state.messages:
        if st.button("🗑️ Limpar Conversa", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.votes = {}
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.caption("""
    **IAmiga** utiliza:
    - 🧠 Busca Semântica TF-IDF
    - 📚 90+ PDFs do Educa Grana
    - 🔍 Query Rewrite + Re-ranking
    - 👍👎 Sistema de Feedback
    """)

# Header
st.markdown("""
<div class="custom-header">
    <h1>🤖 IAmiga</h1>
    <p>Assistente Virtual Inteligente do Educa Grana</p>
</div>
""", unsafe_allow_html=True)

# Imagem logo abaixo do header
image_path = Path(__file__).parent / "assets" / "imagem1.png"
if image_path.exists():
    image_base64 = get_image_base64(image_path)
    if image_base64:
        st.markdown(f"""
        <div style="display:flex; justify-content:center; align-items:center; margin-top:1rem; margin-bottom:2rem;">
            <img src="data:image/png;base64,{image_base64}" 
                 alt="Logo IAmiga"
                 style="max-width:220px; width:100%; height:auto; background:transparent; border:0; outline:none; box-shadow:none;">
        </div>
        """, unsafe_allow_html=True)

# Histórico de mensagens
if not st.session_state.messages:
    st.info("👋 Olá! Sou a IAmiga. Faça sua primeira pergunta sobre o Educa Grana abaixo!")
else:
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message['content'])
            
            # Botões de feedback apenas para respostas do assistente
            if message["role"] == "assistant":
                col1, col2, col3 = st.columns([0.08, 0.08, 0.84])
                with col1:
                    if st.button("👍", key=f"up_{idx}", help="Resposta útil"):
                        st.session_state.votes[idx] = "up"
                        log_vote(message.get("question", ""), "up", message.get("doc_ids", []))
                        st.toast("✅ Obrigado pelo feedback!", icon="✅")
                with col2:
                    if st.button("👎", key=f"down_{idx}", help="Resposta não útil"):
                        st.session_state.votes[idx] = "down"
                        log_vote(message.get("question", ""), "down", message.get("doc_ids", []))
                        st.toast("🔧 Vamos melhorar!", icon="🔧")
                with col3:
                    if idx in st.session_state.votes:
                        vote_emoji = "👍" if st.session_state.votes[idx] == "up" else "👎"
                        st.caption(f"Seu voto: {vote_emoji}")

# Área de input (sempre embaixo)
st.markdown("---")

with st.form(key="question_form", clear_on_submit=True):
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        user_input = st.text_input(
            "Sua pergunta:",
            key="question_input", 
            label_visibility="collapsed",
            placeholder="💬 Digite sua pergunta sobre o Educa Grana..."
        )
    with col2:
        submit = st.form_submit_button("🚀 Enviar", use_container_width=True, type="primary")

# Processar pergunta
if submit and user_input:
    # Adicionar pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Processar resposta
    with st.spinner("🧠 Processando com busca semântica..."):
        try:
            logger.info(f"[APP] Enviando pergunta: {user_input}")
            response = answer_question(user_input)
            logger.info(f"[APP] Resposta recebida: {len(response)} caracteres")
            
            message_data = {
                "role": "assistant", 
                "content": response,
                "question": user_input,
                "doc_ids": []
            }
            st.session_state.messages.append(message_data)
            st.rerun()
        except Exception as e:
            error_msg = f"❌ Erro ao processar: {str(e)}"
            logger.error(f"[APP] Erro: {e}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg,
                "question": user_input,
                "doc_ids": []
            })
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.85em; margin-top: 1rem;'>
    🤖 <strong>IAmiga</strong> - Assistente RAG para Educa Grana | 
    🧠 Busca Semântica TF-IDF | 
    📚 1.035 documentos indexados
</p>
""", unsafe_allow_html=True)
