"""
Interface Streamlit para o Sistema RAG IAmiga
"""
import os
import sys
import time
from pathlib import Path
import importlib
import streamlit as st
import base64  # ← NOVO IMPORT


# Configuração da página
st.set_page_config(
    page_title="IAmiga",
    #page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Função para carregar CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Arquivo styles.css não encontrado!")

# ← NOVA FUNÇÃO
def load_image_as_base64(image_path):
    """Converte imagem para base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"Imagem não encontrada: {image_path}")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar imagem: {e}")
        return None

# Carregar estilos
load_css()

# ← HEADER MODIFICADO
# Header customizado com logo
logo_path = Path(__file__).parent / "assets" / "imagem1.jpeg"
logo_base64 = load_image_as_base64(logo_path)

if logo_base64:
    # Header com logo
    st.markdown(
        f"""
        <div class="custom-header fade-in">
            <div class="main-logo" style="background-image: url(data:image/jpeg;base64,{logo_base64}); width: 80px; height: 80px; background-size: cover; background-position: center; border-radius: 50%; margin: 0 auto 1rem auto; box-shadow: 0 4px 15px rgba(0,0,0,0.2);"></div>
            <h1>IAmiga</h1>
            <p>Sua assistente inteligente para documentos Educa Grana</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Fallback sem logo
    st.markdown(
        """
        <div class="custom-header fade-in">
            <h1>IAmiga</h1>
            <p>Sua assistente inteligente para documentos Educa Grana</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Configurar o path para importar o agent (apenas uma vez, com guarda)
current_dir = Path(__file__).parent           # src/core/frontend/
src_dir = current_dir.parent.parent           # src/
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Importar o agent
try:
    import agent_old
    importlib.reload(agent_old)  # reload para desenvolvimento
    from agent_old import answer_question
    agent_available = True
    print("✅ Agent importado com sucesso")
except ImportError as e:
    st.error(f"Erro ao importar o agent: {e}")
    agent_available = False
except Exception as e:
    st.error(f"Erro geral ao carregar o agent: {e}")
    agent_available = False

# --- CSS PERSONALIZADO ---
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
    }
    .user-message {
        border-left-color: #ff6b6b;
        background-color: #ffe6e6;
    }
    .assistant-message {
        border-left-color: #4ecdc4;
        background-color: #e6fffe;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- HEADER PRINCIPAL ---
st.markdown('<h1 class="main-header">IAmiga - Assistente RAG</h1>', unsafe_allow_html=True)

# Utilitário: status de ambiente sem expor segredos
def env_status():
    from dotenv import load_dotenv
    load_dotenv(override=True)
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    return "✅ OPENAI_API_KEY: presente" if has_key else "❌ OPENAI_API_KEY: ausente"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 📄 Informações do Sistema")

    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown("**🎯 Sobre o IAmiga:**")
    st.markdown("- Sistema RAG para documentos Educa Grana")
    st.markdown("- Base de conhecimento atualizada")
    st.markdown("- Respostas baseadas em contexto")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 🔧 Status do Sistema")
    if agent_available:
        st.success("✅ Agent RAG: Operacional")
    else:
        st.error("❌ Agent RAG: Indisponível")

    st.caption(env_status())

    st.markdown("## 💡 Dicas de Uso")
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown("**Perguntas sugeridas:**")
    st.markdown("- O que é o Educa Grana?")
    st.markdown("- Como funciona a avaliação de carteira?")
    st.markdown("- Quais são as orientações para 2025?")
    st.markdown("- O que são evidências de educação financeira?")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ÁREA PRINCIPAL ---
if not agent_available:
    st.error("🚨 Sistema RAG não disponível. Verifique a configuração do agent.")
    st.stop()

# --- INICIALIZAR HISTÓRICO DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou a IAmiga, sua assistente para documentos do Educa Grana. Como posso ajudá-lo hoje?",
        }
    ]

# --- EXIBIR HISTÓRICO DE CHAT ---
st.markdown("## 💬 Conversa")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message"><strong>👤 Você:</strong><br>{message["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-message assistant-message"><strong>🤖 IAmiga:</strong><br>{message["content"]}</div>',
            unsafe_allow_html=True,
        )

# --- INPUT DO USUÁRIO ---
st.markdown("## ✅ Faça sua pergunta")

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "Digite sua pergunta:",
            placeholder="Ex: O que é o Educa Grana?",
            label_visibility="collapsed",
        )

    with col2:
        submit_button = st.form_submit_button("Enviar 🚀", use_container_width=True)

# --- PROCESSAR PERGUNTA ---
if submit_button and user_input:
    # Adicionar pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibir pergunta do usuário
    st.markdown(
        f'<div class="chat-message user-message"><strong>👤 Você:</strong><br>{user_input}</div>',
        unsafe_allow_html=True,
    )

    # Mostrar loading
    with st.spinner("🤖 Processando sua pergunta..."):
        try:
            start_time = time.time()
            response = answer_question(user_input)
            end_time = time.time()

            # Adicionar resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Exibir resposta
            st.markdown(
                f'<div class="chat-message assistant-message"><strong>🤖 IAmiga:</strong><br>{response}</div>',
                unsafe_allow_html=True,
            )

            # Mostrar tempo de resposta
            response_time = round(end_time - start_time, 2)
            st.caption(f"⏱️ Tempo de resposta: {response_time}s")

        except Exception as e:
            error_msg = f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)

# --- BOTÕES DE AÇÃO ---
st.markdown("## 🔧 Ações")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Limpar Conversa", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversa limpa! Como posso ajudá-lo agora?"}
        ]
        st.rerun()

with col2:
    if st.button("📊 Estatísticas", use_container_width=True):
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.info(f"📈 Total de mensagens: {total_messages}\n👤 Suas perguntas: {user_messages}")

with col3:
    if st.button("💾 Exportar Chat", use_container_width=True):
        chat_export = "\n".join(
            [
                f"{'👤 VOCÊ' if m['role'] == 'user' else '🤖 IAmiga'}: {m['content']}"
                for m in st.session_state.messages
            ]
        )
        st.download_button(
            label="📥 Download do Chat",
            data=chat_export,
            file_name="chat_IAmiga.txt",
            mime="text/plain",
        )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🤖 IAmiga - Assistente RAG para Educa Grana | "
    "Desenvolvido com Streamlit + LangChain + OpenAI"
    "</div>",
    unsafe_allow_html=True,
)