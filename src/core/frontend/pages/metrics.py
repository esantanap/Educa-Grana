# src/core/frontend/metrics.py - Página de Métricas e Monitoramento
import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime
from collections import Counter
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide", page_title="IAmiga - Métricas", page_icon="📊")

def load_telemetry_data():
    """Carregar dados de telemetria e guardrails"""
    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    telemetry_path = data_dir / "telemetry.log"
    guardrails_path = data_dir / "guardrails.log"
    
    telemetry = []
    guardrails = []
    
    # Carregar telemetria
    if telemetry_path.exists():
        try:
            with open(telemetry_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        telemetry.append(json.loads(line.strip()))
                    except:
                        pass
        except Exception as e:
            logger.warning(f"Erro ao carregar telemetria: {e}")
    
    # Carregar guardrails
    if guardrails_path.exists():
        try:
            with open(guardrails_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        guardrails.append(json.loads(line.strip()))
                    except:
                        pass
        except Exception as e:
            logger.warning(f"Erro ao carregar guardrails: {e}")
    
    return telemetry, guardrails

def analyze_metrics(telemetry, guardrails):
    """Analisar métricas de telemetria e guardrails"""
    queries = [e for e in telemetry if e.get('event') == 'query']
    votes = [e for e in telemetry if e.get('event') == 'vote']
    
    # Métricas gerais
    total_events = len(telemetry)
    total_queries = len(queries)
    total_votes = len(votes)
    
    # Análise de expansão
    expanded_queries = sum(1 for q in queries if q.get('expanded_query') and q.get('expanded_query') != q.get('q'))
    expansion_rate = (expanded_queries / total_queries * 100) if total_queries > 0 else 0
    
    # Análise de votos
    upvotes = sum(1 for v in votes if v.get('vote') == 'up')
    downvotes = sum(1 for v in votes if v.get('vote') == 'down')
    satisfaction_rate = (upvotes / total_votes * 100) if total_votes > 0 else 0
    
    # Análise de busca
    avg_results = sum(q.get('results_count', 0) for q in queries) / total_queries if total_queries > 0 else 0
    
    # Top queries
    query_texts = [q.get('q', '') for q in queries]
    top_queries = Counter(query_texts).most_common(10)
    
    # Análise de guardrails
    total_violations = len(guardrails)
    input_violations = sum(1 for g in guardrails if g.get('type') == 'input_violation')
    output_violations = sum(1 for g in guardrails if g.get('type') == 'output_violation')
    
    # Tipos de violações
    violation_types = Counter()
    severity_dist = Counter()
    
    for g in guardrails:
        if g.get('type') == 'input_violation':
            for v in g.get('violations', []):
                violation_types[v.get('type', 'unknown')] += 1
                severity_dist[v.get('severity', 'unknown')] += 1
        elif g.get('type') == 'output_violation':
            violation_types[g.get('violation_type', 'unknown')] += 1
            severity_dist[g.get('severity', 'unknown')] += 1
    
    # Top blocked questions
    blocked_questions = Counter()
    for g in guardrails:
        if g.get('type') == 'input_violation':
            q = g.get('question', '')[:100]
            blocked_questions[q] += 1
    
    return {
        'total_events': total_events,
        'total_queries': total_queries,
        'total_votes': total_votes,
        'expansion_rate': expansion_rate,
        'expanded_queries': expanded_queries,
        'upvotes': upvotes,
        'downvotes': downvotes,
        'satisfaction_rate': satisfaction_rate,
        'avg_results': avg_results,
        'top_queries': top_queries,
        'total_violations': total_violations,
        'input_violations': input_violations,
        'output_violations': output_violations,
        'violation_types': dict(violation_types.most_common()),
        'severity_dist': dict(severity_dist.most_common()),
        'top_blocked': blocked_questions.most_common(10)
    }

# CSS
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    .main .block-container {
        padding-top: 1rem;
        max-width: 100%;
    }
    
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
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("###  Atualização")
    if st.button("🔄 Recarregar Dados", width="stretch", type="primary"):
        st.rerun()
    st.caption(f"⏰ {datetime.now().strftime('%H:%M:%S')}")

# Header
st.markdown("""
<div class="custom-header">
    <h1>📊 Métricas e Monitoramento - IAmiga</h1>
    <p>Dashboard em tempo real do sistema | 🧪 Ambiente: PILOTO</p>
</div>
""", unsafe_allow_html=True)

# Carregar dados
telemetry, guardrails = load_telemetry_data()
metrics = analyze_metrics(telemetry, guardrails)

# Métricas Gerais
st.subheader("📈 Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total de Eventos", metrics['total_events'])
with col2:
    st.metric("💬 Queries Processadas", metrics['total_queries'])
with col3:
    st.metric("👍👎 Votos Recebidos", metrics['total_votes'])
with col4:
    st.metric("😊 Satisfação", f"{metrics['satisfaction_rate']:.1f}%", 
              delta=f"{metrics['upvotes']} 👍 / {metrics['downvotes']} 👎")

st.markdown("---")

# Expansão de Queries
st.subheader("🔄 Expansão de Queries")
col1, col2 = st.columns([0.3, 0.7])
with col1:
    st.metric("Taxa de Expansão", f"{metrics['expansion_rate']:.1f}%")
    st.metric("Queries Expandidas", f"{metrics['expanded_queries']}/{metrics['total_queries']}")
    st.metric("Média de Resultados", f"{metrics['avg_results']:.1f}")
with col2:
    if metrics['top_queries']:
        st.write("**Top 10 Queries Mais Frequentes:**")
        df_queries = []
        for q, count in metrics['top_queries']:
            df_queries.append({"Pergunta": q[:80], "Frequência": count})
        st.dataframe(df_queries, width="stretch", hide_index=True)

st.markdown("---")

# Guardrails e Segurança
st.subheader("🛡️ Guardrails - Segurança e Proteção")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("⚠️ Total de Violações", metrics['total_violations'])
with col2:
    st.metric("🛡️ Entradas Bloqueadas", metrics['input_violations'])
with col3:
    st.metric("🚫 Saídas Filtradas", metrics['output_violations'])

if metrics['total_violations'] > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Tipos de Violações:**")
        if metrics['violation_types']:
            df_violations = []
            for vtype, count in metrics['violation_types'].items():
                df_violations.append({"Tipo": vtype, "Frequência": count})
            st.dataframe(df_violations, width="stretch", hide_index=True)
    
    with col2:
        st.write("**Distribuição por Severidade:**")
        if metrics['severity_dist']:
            df_severity = []
            for severity, count in metrics['severity_dist'].items():
                emoji = "🔴" if severity == "critical" else "🟠" if severity == "high" else "🟡" if severity == "medium" else "🟢"
                df_severity.append({"Severidade": f"{emoji} {severity.upper()}", "Ocorrências": count})
            st.dataframe(df_severity, width="stretch", hide_index=True)
    
    if metrics['top_blocked']:
        st.write("**Perguntas Mais Bloqueadas (Top 10):**")
        df_blocked = []
        for q, count in metrics['top_blocked']:
            df_blocked.append({"Pergunta": q, "Bloqueios": count})
        st.dataframe(df_blocked, width="stretch", hide_index=True)
else:
    st.success("✅ Nenhuma violação detectada. Sistema operando normalmente!")

st.markdown("---")
st.caption("ℹ️ Os dados são atualizados em tempo real a partir dos logs do sistema. Para visualizar o relatório HTML completo, execute `python scripts/analyze_telemetry.py` e abra o arquivo `data/telemetry_report.html`.")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #999; font-size: 0.85em;'>
    🤖 <strong>IAmiga</strong> - Sistema de Métricas e Monitoramento | 
    🔄 Dados atualizados em tempo real | 
    🧪 Ambiente: PILOTO
</p>
""", unsafe_allow_html=True)
