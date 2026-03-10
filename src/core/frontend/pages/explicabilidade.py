"""
Painel de Explicabilidade (XAI) - IAmiga
Mostra em tempo real como o sistema está tomando decisões.
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(
    page_title="Explicabilidade XAI - IAmiga",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Explicabilidade (XAI) - IAmiga")
st.markdown("Veja em tempo real como o sistema toma decisões e gera respostas")

# Link para glossário
with st.expander("📖 Entenda as Métricas de Explicabilidade", expanded=False):
    st.markdown("""
    ### 🎯 Glossário de Explicabilidade (XAI)
    
    #### **✏️ Query Rewrite (Reescrita de Query)**
    **O que é:** Processo de expandir a pergunta original com sinônimos e termos relacionados.
    
    **Por que importa:** Melhora a busca ao encontrar documentos que usam palavras diferentes mas com mesmo significado.
    
    **Exemplo:** "empréstimo" → "empréstimo, crédito, financiamento"
    
    ---
    
    #### **📚 Document Retrieval (Recuperação de Documentos)**
    **O que é:** Busca e ranking dos documentos mais relevantes na base de conhecimento.
    
    **Por que importa:** Determina qual contexto será usado para gerar a resposta.
    
    **Métricas:**
    - **Score**: Relevância do documento (0 a 1, quanto maior melhor)
    - **Top-K**: Quantidade de documentos recuperados
    
    ---
    
    #### **📊 Confidence Score (Nível de Confiança)**
    **O que é:** Indicador de quão confiável é a resposta gerada (0-100%).
    
    **Por que importa:** Ajuda a saber quando a resposta pode estar incompleta ou incerta.
    
    **Interpretação:**
    - 🟢 **80-100%**: Alta confiança - resposta bem fundamentada
    - 🟡 **60-79%**: Média confiança - resposta razoável mas com ressalvas
    - 🔴 **0-59%**: Baixa confiança - resposta pode estar incompleta
    
    **Fatores que influenciam:**
    - Score médio dos documentos recuperados
    - Quantidade de documentos relevantes encontrados
    - Cobertura da query pelos documentos
    
    ---
    
    #### **📖 Citations (Citações)**
    **O que é:** Fontes específicas da base de conhecimento usadas na resposta.
    
    **Por que importa:** Permite rastrear de onde veio cada informação, garantindo transparência.
    
    **Como usar:** Verifique as fontes citadas para validar a resposta.
    
    ---
    
    #### **🛡️ Guardrails (Proteções)**
    **O que é:** Validações de segurança aplicadas à entrada (pergunta) e saída (resposta).
    
    **Por que importa:** Protege contra conteúdo inadequado, jailbreaks e tópicos fora do escopo.
    
    **Tipos de bloqueio:**
    - Tentativas de manipulação (jailbreak)
    - Tópicos proibidos (política, religião, conteúdo adulto)
    - Dados sensíveis (CPF, senhas)
    - Perguntas fora do escopo (não relacionadas ao Crediamigo/BNB)
    
    ---
    
    #### **🔮 Counterfactual Explanations (Cenários "E se...?")**
    **O que é:** Explicações mostrando como diferentes perguntas teriam resultados diferentes.
    
    **Por que importa:** Ensina usuários a fazer perguntas melhores e entender o sistema.
    
    **Tipos de cenários:**
    - **No Expansion**: E se não expandisse com sinônimos?
    - **More Specific**: E se adicionasse termos mais específicos?
    - **Remove Vague**: E se removesse termos vagos?
    - **Alternative Focus**: E se mudasse o foco da pergunta?
    - **Result-Based**: Sugestões baseadas no número de resultados obtidos
    
    **Impacto:**
    - ✅ Verde = melhoria esperada
    - ❌ Vermelho = piora esperada
    - ➡️ Azul = neutro
    - 🔄 Amarelo = alternativa válida
    
    ---
    
    ### 💡 Como usar este painel
    
    1. **Filtros**: Use para focar em tipos específicos de eventos
    2. **Auto-refresh**: Ative para monitoramento em tempo real
    3. **Detalhes**: Marque para ver informações completas
    4. **Sessões**: Cada consulta agrupa todos os eventos relacionados
    5. **Timeline**: Visualize o fluxo de processamento de cada query
    
    ---
    
    ### 🎓 Benefícios da Explicabilidade
    
    ✅ **Transparência**: Entenda como decisões são tomadas  
    ✅ **Confiança**: Veja as fontes e validações aplicadas  
    ✅ **Aprendizado**: Melhore suas perguntas com counterfactuals  
    ✅ **Auditoria**: Rastreie o comportamento do sistema  
    ✅ **Debugging**: Identifique problemas no pipeline RAG  
    """)

# Caminho para o arquivo de explicações
base_dir = Path(__file__).parent.parent.parent.parent.parent
xai_log_path = base_dir / "data" / "xai_explanations.log"

# Controles
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    st.markdown("### 📊 Rastreamento de Decisões")

with col2:
    if st.button("🔃 Recarregar", use_container_width=True):
        st.rerun()

with col3:
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)

with col4:
    if auto_refresh:
        refresh_interval = st.number_input("⏱️ Segundos:", 5, 60, 10, 5, label_visibility="collapsed")
    else:
        refresh_interval = 10

# Filtros
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filter_type = st.selectbox(
        "🏷️ Tipo",
        ["Todos", "Query Rewrite", "Document Retrieval", "Confidence Score", "Citation", "Guardrails", "Counterfactual"]
    )

with col_f2:
    max_entries = st.slider("📄 Max. Entradas", 10, 100, 50, 10)

with col_f3:
    show_details = st.checkbox("📋 Mostrar Detalhes", value=True)

st.markdown("---")

def load_xai_logs():
    """Carrega logs de explicabilidade."""
    if not xai_log_path.exists():
        return []
    
    try:
        with open(xai_log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            entries = []
            for line in reversed(lines[-max_entries:]):  # Mais recentes primeiro
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            return entries
    except Exception as e:
        st.error(f"Erro ao ler logs: {e}")
        return []

def group_events_by_query(entries):
    """Agrupa eventos relacionados à mesma query por proximidade temporal."""
    from collections import defaultdict
    from datetime import datetime, timedelta
    
    if not entries:
        return []
    
    groups = []
    current_group = []
    last_timestamp = None
    
    # Agrupar eventos que ocorrem próximos (dentro de 5 segundos)
    for entry in entries:
        try:
            timestamp_str = entry.get('timestamp', '')
            timestamp = datetime.fromisoformat(timestamp_str)
            
            if last_timestamp is None or (last_timestamp - timestamp).total_seconds() > 5:
                # Novo grupo
                if current_group:
                    groups.append(current_group)
                current_group = [entry]
            else:
                # Adicionar ao grupo atual
                current_group.append(entry)
            
            last_timestamp = timestamp
        except:
            # Se houver erro, criar novo grupo
            if current_group:
                groups.append(current_group)
            current_group = [entry]
    
    # Adicionar último grupo
    if current_group:
        groups.append(current_group)
    
    return groups

def render_query_rewrite(entry):
    """Renderiza explicação de reescrita de query."""
    with st.expander(f"🔄 Query Rewrite - {entry.get('timestamp', 'N/A')}", expanded=False):
        original = entry.get('original_query', 'N/A')
        rewritten = entry.get('rewritten_query', 'N/A')
        added_terms = entry.get('added_terms', [])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Query Original:**")
            st.code(original, language=None)
        with col2:
            st.markdown("**Query Expandida:**")
            st.code(rewritten, language=None)
        
        if added_terms:
            st.markdown("**Termos Adicionados:**")
            st.write(", ".join([f"`{t}`" for t in added_terms]))
        
        if show_details and entry.get('explanation'):
            st.markdown("**Explicação:**")
            st.info(entry['explanation'])

def render_query_rewrite_compact(entry):
    """Versão compacta de query rewrite."""
    original = entry.get('original_query', 'N/A')
    rewritten = entry.get('rewritten_query', 'N/A')
    added_terms = entry.get('added_terms', [])
    
    st.markdown("**✏️ Query Rewrite**")
    if added_terms:
        st.success(f"✅ Expandida com {len(added_terms)} termos: {', '.join(added_terms[:3])}")
    else:
        st.info("➡️ Sem expansão necessária")
    
    if show_details:
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Original:")
            st.code(original[:100], language=None)
        with col2:
            st.caption("Expandida:")
            st.code(rewritten[:100], language=None)

def render_document_retrieval(entry):
    """Renderiza explicação de recuperação de documentos."""
    with st.expander(f"📚 Document Retrieval - {entry.get('timestamp', 'N/A')}", expanded=False):
        docs = entry.get('retrieved_docs', [])
        query = entry.get('query', 'N/A')
        
        st.markdown(f"**Query:** `{query}`")
        st.markdown(f"**Documentos Recuperados:** {len(docs)}")
        
        if docs and show_details:
            for i, doc in enumerate(docs[:5], 1):  # Top 5
                score = doc.get('score', 0)
                snippet = doc.get('snippet', '')[:200] + '...'
                
                st.markdown(f"**{i}. Score: {score:.3f}**")
                st.text(snippet)
                if doc.get('matched_terms'):
                    st.caption(f"Termos: {', '.join(doc['matched_terms'])}")
                st.markdown("---")

def render_document_retrieval_compact(entry):
    """Versão compacta de document retrieval."""
    docs = entry.get('retrieved_docs', [])
    total = entry.get('total_available', 'N/A')
    
    st.markdown("**📚 Document Retrieval**")
    st.info(f"📄 Recuperados {len(docs)} de {total} documentos")
    
    if docs and show_details:
        avg_score = sum(d.get('score', 0) for d in docs[:5]) / min(5, len(docs))
        st.metric("Score Médio (Top 5)", f"{avg_score:.3f}")

def render_confidence_score(entry):
    """Renderiza explicação de confidence score."""
    with st.expander(f"📊 Confidence Score - {entry.get('timestamp', 'N/A')}", expanded=False):
        score = entry.get('confidence', 0)
        factors = entry.get('factors', {})
        
        # Barra de progresso colorida
        if score >= 0.8:
            color = "🟢"
        elif score >= 0.6:
            color = "🟡"
        else:
            color = "🔴"
        
        st.markdown(f"### {color} Confiança: {score*100:.1f}%")
        st.progress(score)
        
        if factors and show_details:
            st.markdown("**Fatores:**")
            for factor, value in factors.items():
                st.markdown(f"- **{factor}**: {value}")

def render_confidence_score_compact(entry):
    """Versão compacta de confidence score."""
    score = entry.get('confidence', 0)
    
    st.markdown("**📊 Confidence Score**")
    
    if score >= 0.8:
        st.success(f"🟢 Alta confiança: {score*100:.1f}%")
    elif score >= 0.6:
        st.warning(f"🟡 Média confiança: {score*100:.1f}%")
    else:
        st.error(f"🔴 Baixa confiança: {score*100:.1f}%")

def render_citation(entry):
    """Renderiza explicação de citações."""
    with st.expander(f"📖 Citations - {entry.get('timestamp', 'N/A')}", expanded=False):
        citations = entry.get('citations', [])
        
        st.markdown(f"**Total de Citações:** {len(citations)}")
        
        if citations and show_details:
            for i, cite in enumerate(citations, 1):
                st.markdown(f"**[{i}]** {cite.get('source', 'N/A')}")
                st.caption(cite.get('text', '')[:150] + '...')

def render_citation_compact(entry):
    """Versão compacta de citation."""
    citations = entry.get('citations', [])
    
    st.markdown("**📖 Citations**")
    st.info(f"📑 {len(citations)} fontes citadas")
    
    if citations and show_details:
        sources = [c.get('source', 'N/A') for c in citations[:3]]
        st.caption(f"Top 3: {', '.join(sources)}")

def render_guardrails(entry):
    """Renderiza explicação de guardrails."""
    with st.expander(f"🛡️ Guardrails - {entry.get('timestamp', 'N/A')}", expanded=False):
        passed = entry.get('passed', True)
        violations = entry.get('violations', [])
        
        if passed:
            st.success("✅ Validação Passou")
        else:
            st.error("❌ Validação Bloqueada")
        
        if violations and show_details:
            st.markdown("**Violações:**")
            for v in violations:
                st.markdown(f"- **{v.get('type')}** ({v.get('severity')}): {v.get('message')}")

def render_guardrails_compact(entry):
    """Versão compacta de guardrails."""
    passed = entry.get('passed', True)
    violations = entry.get('violations', [])
    
    st.markdown("**🛡️ Guardrails**")
    if passed:
        st.success("✅ Validação OK")
    else:
        st.error(f"❌ Bloqueado ({len(violations)} violações)")

def render_counterfactual(entry):
    """Renderiza explicações contrafactuais."""
    with st.expander(f"🔮 Counterfactual - {entry.get('timestamp', 'N/A')}", expanded=True):
        query = entry.get('query', 'N/A')
        counterfactuals = entry.get('counterfactuals', [])
        
        st.markdown(f"**Query Original:** `{query}`")
        st.markdown(f"**Cenários 'E se...?':** {len(counterfactuals)}")
        
        if not counterfactuals:
            st.warning("⚠️ Nenhum cenário contrafactual foi gerado para esta query")
            return
        
        st.markdown("---")
        
        # Sempre mostrar os counterfactuals
        for i, cf in enumerate(counterfactuals, 1):
            impact = cf.get('impact', 'neutral')
            cf_type = cf.get('type', 'unknown')
            
            # Emoji baseado no impacto
            emoji_map = {
                'positive': '✅',
                'negative': '❌',
                'neutral': '➡️',
                'alternative': '🔄'
            }
            emoji = emoji_map.get(impact, '💡')
            
            # Cor baseada no impacto
            color_map = {
                'positive': '#d4edda',
                'negative': '#f8d7da',
                'neutral': '#e7f3ff',
                'alternative': '#fff3cd'
            }
            bg_color = color_map.get(impact, '#f0f0f0')
            
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                        <h4>{emoji} Cenário {i}: {cf_type.replace('_', ' ').title()}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📝 Original:**")
                    st.code(cf.get('original', 'N/A'), language=None)
                with col2:
                    st.markdown("**🔀 Variação:**")
                    st.code(cf.get('variation', 'N/A'), language=None)
                
                st.info(f"💡 {cf.get('message', '')}")
                
                # Informações extras
                if 'terms_affected' in cf:
                    st.caption(f"Termos afetados: {', '.join(cf['terms_affected'])}")
                elif 'suggested_terms' in cf:
                    st.caption(f"Termos sugeridos: {cf['suggested_terms']}")
                
                st.markdown("---")

def render_counterfactual_compact(entry):
    """Versão compacta de counterfactual."""
    counterfactuals = entry.get('counterfactuals', [])
    
    st.markdown("**🔮 Counterfactual Explanations**")
    
    if not counterfactuals:
        st.caption("⚠️ Nenhum cenário gerado")
        return
    
    st.info(f"💡 {len(counterfactuals)} cenários 'E se...?' gerados")
    
    # Sempre mostrar resumo dos counterfactuals
    if counterfactuals:
        # Mostrar cards compactos para cada cenário
        for i, cf in enumerate(counterfactuals[:3], 1):  # Mostrar top 3
            impact = cf.get('impact', 'neutral')
            emoji_map = {
                'positive': '✅',
                'negative': '❌',
                'neutral': '➡️',
                'alternative': '🔄'
            }
            emoji = emoji_map.get(impact, '💡')
            
            st.markdown(f"{emoji} **{i}.** {cf.get('message', 'N/A')[:80]}...")
        
        if len(counterfactuals) > 3:
            st.caption(f"+ {len(counterfactuals) - 3} cenários adicionais")

# Carregar logs
entries = load_xai_logs()

if not xai_log_path.exists():
    st.warning("⚠️ Arquivo de explicações ainda não foi criado. Execute algumas queries primeiro!")
    st.info(f"📂 Arquivo esperado: `{xai_log_path}`")
elif not entries:
    st.info("ℹ️ Nenhuma explicação registrada ainda. Execute queries no assistente principal.")
else:
    # Filtrar por tipo
    if filter_type != "Todos":
        type_map = {
            "Query Rewrite": "query_rewrite",
            "Document Retrieval": "document_retrieval",
            "Confidence Score": "confidence_score",
            "Citation": "citation",
            "Guardrails": "guardrails",
            "Counterfactual": "counterfactual"
        }
        entries = [e for e in entries if e.get('type') == type_map.get(filter_type)]
    
    # Estatísticas
    st.markdown("### 📊 Estatísticas")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    with col_s1:
        st.metric("Total de Eventos", len(entries))
    with col_s2:
        query_rewrites = len([e for e in entries if e.get('type') == 'query_rewrite'])
        st.metric("Query Rewrites", query_rewrites)
    with col_s3:
        retrievals = len([e for e in entries if e.get('type') == 'document_retrieval'])
        st.metric("Retrievals", retrievals)
    with col_s4:
        guardrails_checked = len([e for e in entries if e.get('type') == 'guardrails'])
        st.metric("Guardrails", guardrails_checked)
    
    # Adicionar estatística de counterfactuals se houver
    if any(e.get('type') == 'counterfactual' for e in entries):
        col_s5, _, _, _ = st.columns(4)
        with col_s5:
            counterfactuals_count = len([e for e in entries if e.get('type') == 'counterfactual'])
            st.metric("Counterfactuals", counterfactuals_count)
    
    st.markdown("---")
    st.markdown("### 📋 Histórico de Explicações")
    
    # Agrupar eventos por query
    event_groups = group_events_by_query(entries)
    
    st.info(f"📦 {len(event_groups)} sessões de consulta encontradas")
    
    # Renderizar grupos
    for group_idx, group in enumerate(event_groups, 1):
        # Extrair informações do grupo
        query_text = "N/A"
        timestamp = "N/A"
        
        # Pegar query do primeiro evento relevante
        for entry in group:
            if entry.get('type') == 'query_rewrite':
                query_text = entry.get('original_query', 'N/A')
                timestamp = entry.get('timestamp', 'N/A')
                break
            elif entry.get('query'):
                query_text = entry.get('query', 'N/A')
                timestamp = entry.get('timestamp', 'N/A')
                break
        
        # Estatísticas do grupo
        types_in_group = [e.get('type') for e in group]
        type_counts = {t: types_in_group.count(t) for t in set(types_in_group)}
        
        # Header do grupo com resumo
        with st.expander(f"🔍 Consulta #{group_idx} - {query_text[:60]}... ({timestamp[:19]})", expanded=(group_idx == 1)):
            # Resumo visual do fluxo
            st.markdown("#### 🔄 Fluxo de Processamento")
            
            cols = st.columns(len(group))
            for idx, (col, entry) in enumerate(zip(cols, group)):
                with col:
                    entry_type = entry.get('type', 'unknown')
                    type_emoji = {
                        'query_rewrite': '✏️',
                        'document_retrieval': '📚',
                        'confidence_score': '📊',
                        'citation': '📖',
                        'guardrails': '🛡️',
                        'counterfactual': '🔮'
                    }
                    emoji = type_emoji.get(entry_type, '❓')
                    st.markdown(f"**{idx+1}. {emoji}**")
                    st.caption(entry_type.replace('_', ' ').title())
            
            st.markdown("---")
            st.markdown("#### 📄 Detalhes dos Eventos")
            
            # Renderizar cada entrada do grupo
            for entry in group:
                entry_type = entry.get('type', 'unknown')
                
                if entry_type == 'query_rewrite':
                    render_query_rewrite_compact(entry)
                elif entry_type == 'document_retrieval':
                    render_document_retrieval_compact(entry)
                elif entry_type == 'confidence_score':
                    render_confidence_score_compact(entry)
                elif entry_type == 'citation':
                    render_citation_compact(entry)
                elif entry_type == 'guardrails':
                    render_guardrails_compact(entry)
                elif entry_type == 'counterfactual':
                    render_counterfactual_compact(entry)
                else:
                    st.json(entry)

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
