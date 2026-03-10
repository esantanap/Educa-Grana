# test_feedback_loop.py
"""
Testa o sistema de feedback loop com dados simulados.
Gera telemetria adicional para demonstrar as funcionalidades.
"""

import json
from pathlib import Path
from datetime import datetime

# Simular eventos de telemetria
telemetry_file = Path("data/telemetry_test.log")

# Criar dados de teste
test_events = [
    # Queries com expansão
    {
        "event": "query_rewrite_rerank",
        "original_query": "Quais os prazos das operações?",
        "expanded_query": "quai os prazo das operacao emprestimo contrato ccb",
        "added_terms": ["emprestimo", "contrato", "ccb"],
        "num_results": 5,
        "search_type": "semântica"
    },
    {
        "event": "query_rewrite_rerank",
        "original_query": "Como funciona o empréstimo?",
        "expanded_query": "como funciona o emprestimo operacao contrato ccb",
        "added_terms": ["operacao", "contrato", "ccb"],
        "num_results": 5,
        "search_type": "semântica"
    },
    {
        "event": "query_rewrite_rerank",
        "original_query": "Documentos necessários para CCB",
        "expanded_query": "documento necessario para ccb",
        "added_terms": [],
        "num_results": 5,
        "search_type": "semântica"
    },
    {
        "event": "query_rewrite_rerank",
        "original_query": "Qual a taxa de juros?",
        "expanded_query": "qual a taxa de juro",
        "added_terms": [],
        "num_results": 4,
        "search_type": "semântica"
    },
    {
        "event": "query_rewrite_rerank",
        "original_query": "Crediamigo tem limite máximo?",
        "expanded_query": "crediamigo tem limite maximo",
        "added_terms": [],
        "num_results": 3,
        "search_type": "semântica"
    },
    # Votos
    {
        "event": "vote",
        "vote": "up",
        "question": "Quais os prazos das operações?",
        "doc_ids": ["1102-procedimento-prazos.pdf", "normativo-credito.pdf"]
    },
    {
        "event": "vote",
        "vote": "up",
        "question": "Como funciona o empréstimo?",
        "doc_ids": ["1102-procedimento-emprestimo.pdf"]
    },
    {
        "event": "vote",
        "vote": "down",
        "question": "Documentos necessários para CCB",
        "doc_ids": ["apresentacao-geral.pdf", "e-book01.pdf"]
    },
    {
        "event": "vote",
        "vote": "down",
        "question": "Qual a taxa de juros?",
        "doc_ids": ["apresentacao-produtos.pdf"]
    },
    {
        "event": "vote",
        "vote": "up",
        "question": "Crediamigo tem limite máximo?",
        "doc_ids": ["1102-procedimento-limites.pdf", "normativo-limites.pdf"]
    },
]

# Salvar eventos de teste
with open(telemetry_file, 'w', encoding='utf-8') as f:
    for event in test_events:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')

print(f"✅ Criados {len(test_events)} eventos de teste em {telemetry_file}")

# Executar análise com dados de teste
print("\n" + "=" * 80)
print("🧪 EXECUTANDO ANÁLISE COM DADOS DE TESTE")
print("=" * 80)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from analyze_telemetry import TelemetryAnalyzer
from suggest_glossary_updates import GlossarySuggester

# Análise
analyzer = TelemetryAnalyzer(telemetry_path="data/telemetry_test.log")
analyzer.load_data()
html_report = analyzer.generate_report(output_path="data/telemetry_test_report.html")

# Sugestões
suggester = GlossarySuggester(telemetry_path="data/telemetry_test.log")
suggester.load_telemetry()
md_report = suggester.generate_suggestions_report(output_path="data/glossary_test_suggestions.md")

print("\n" + "=" * 80)
print("✅ RELATÓRIOS DE TESTE GERADOS")
print("=" * 80)
print(f"📊 HTML: {html_report}")
print(f"📝 MD: {md_report}")
print("\nAbra os arquivos para ver exemplos completos!")
