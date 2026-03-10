# app.py
import streamlit as st
import sys
from pathlib import Path
import base64

st.set_page_config(layout="wide", page_title="IAmiga - Assistente RAG")

def get_image_base64(image_path: Path) -> str:
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return ""

# Carregar CSS externo
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("styles.css não encontrado. As estilizações podem não ser aplicadas.")

# Caminho do src para importar o agent
current_dir = Path(__file__).parent.parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Importar agent
try:
    from agent_old import answer_question
except ImportError as e:
    st.error(f"❌ Erro ao importar agent: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Informações do Sistema")
    st.markdown("- Sobre o IAmiga:")
    st.markdown("  - Sistema RAG para documentos Educa Grana")
    st.markdown("  - Base de conhecimento atualizada")
    st.markdown("  - Respostas baseadas em contexto")

    st.header("Status do Sistema")
    st.success("✔ Agent RAG: Operacional")
    st.success("✔ OPENAI_API_KEY: presente")

    st.header("Dicas de Uso")
    st.info("Perguntas sugeridas:")
    st.markdown("- O que é o Educa Grana?")

# Header centralizado com gradiente e conteúdo
with st.container():
    # Remove quaisquer sombras/bordas herdadas da classe antiga
    st.markdown("""
    <style>
      .header-image, .header-image * {
        border: 0 !important;
        outline: none !important;
        box-shadow: none !important;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-header-block'><div class='center-header'>", unsafe_allow_html=True)

    # IMAGEM AGORA EM PNG, SEM CÍRCULO
    image_path = Path(__file__).parent / "assets" / "imagem1.png"
    if image_path.exists():
        image_base64 = get_image_base64(image_path)
        if image_base64:
            st.markdown(
                f"""
                <div class='header-image' style="display:flex; justify-content:center; align-items:center;">
                    <img src="data:image/png;base64,{image_base64}"
                         alt="Logo IAmiga"
                         style="max-width:220px; width:100%; height:auto; background:transparent; border:0; outline:none; box-shadow:none;">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class='header-image' style="display:flex; justify-content:center; align-items:center;">
                    <div style="color:#999; font-size:14px;">
                        Erro ao carregar imagem
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class='header-image' style="display:flex; justify-content:center; align-items:center;">
                <div style="color:#999; font-size:14px;">
                    Imagem não encontrada
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # TÍTULO E SUBTÍTULO
    st.markdown(
        """
        <div class='header-text'>
            <h1 class='header-title'>IAmiga</h1>
            <p class='header-subtitle'>Sua assistente inteligente para documentos Educa Grana</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div></div>", unsafe_allow_html=True)

# app.py (trecho a substituir: seção de perguntas / histórico / expander)
# Histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título da seção de perguntas (permanece)
st.markdown("### 💬 Faça sua pergunta:")

# FORMULÁRIO POSICIONADO IMEDIATAMENTE APÓS O TÍTULO
with st.form(key="question_form", clear_on_submit=True):
    user_input = st.text_input("Digite sua pergunta sobre Educa Grana...", key="question_input")
    submit = st.form_submit_button("Enviar")

    # Se desejar estilo inline do botão, altere acima; o form mantém a entrada no local desejado.

# Processamento da pergunta quando o usuário clica em Enviar
if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibe pergunta do usuário
    with st.chat_message("user"):
        st.markdown(f"<div class='user-message-25'>{user_input}</div>", unsafe_allow_html=True)

    # Resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = answer_question(user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ Erro ao processar pergunta: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Divider e exibição do histórico logo abaixo do formulário
st.markdown("---")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div class='user-message-25'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# Botão para limpar conversa
if st.session_state.messages:
    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

# SOBRE A IAMIGA NO FIM DA PÁGINA (RODAPÉ)
with st.expander("ℹ️ Sobre a IAmiga"):
    st.markdown("""
    **IAmiga** é uma assistente especializada em documentos do Educa Grana que utiliza:
    - 🧠 Inteligência Artificial
    - 📚 Base de conhecimento Educa Grana
    - 🔍 Busca semântica
    - 💬 Interface conversacional
    """)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ccc;'>IAmiga - Assistente RAG para Educa Grana | Desenvolvido com Streamlit + LangChain + OpenAI</p>", unsafe_allow_html=True)
