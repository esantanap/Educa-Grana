#!/usr/bin/env python3
# scripts/analyze_telemetry.py
"""
Analisa dados de telemetria para gerar insights sobre o uso do sistema.
Gera relatório HTML com métricas visuais.
"""

import json
import sys
import io
from pathlib import Path

# Configurar stdout para UTF-8 no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

# Adicionar src/ ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from core.search.query_rewriter import normalize_token


class TelemetryAnalyzer:
    def __init__(self, telemetry_path: str = "data/telemetry.log"):
        self.telemetry_path = Path(telemetry_path)
        self.guardrails_path = Path("data/guardrails.log")
        self.events = []
        self.queries = []
        self.votes = []
        self.guardrail_violations = []
        
    def load_data(self):
        """Carrega e separa eventos de telemetria."""
        if not self.telemetry_path.exists():
            print(f"[!] Arquivo {self.telemetry_path} não encontrado")
            return
        
        with open(self.telemetry_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    self.events.append(event)
                    
                    if event.get('event') == 'query_rewrite_rerank':
                        self.queries.append(event)
                    elif event.get('event') == 'vote':
                        self.votes.append(event)
                except json.JSONDecodeError:
                    continue
        
        # Carregar violações de guardrails
        if self.guardrails_path.exists():
            with open(self.guardrails_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        violation = json.loads(line)
                        self.guardrail_violations.append(violation)
                    except json.JSONDecodeError:
                        continue
        
        print(f"✅ Carregados {len(self.events)} eventos ({len(self.queries)} queries, {len(self.votes)} votos)")
        print(f"🛡️  Violações de guardrails: {len(self.guardrail_violations)}")
    
    def analyze_query_expansion(self) -> Dict:
        """Analisa efetividade da expansão de queries."""
        total = len(self.queries)
        expanded = sum(1 for q in self.queries if q.get('added_terms'))
        expansion_rate = (expanded / total * 100) if total > 0 else 0
        
        # Termos mais adicionados
        all_terms = []
        for q in self.queries:
            all_terms.extend(q.get('added_terms', []))
        term_counter = Counter(all_terms)
        
        # Queries que não expandiram mas talvez devessem
        no_expansion = [q.get('original_query') for q in self.queries if not q.get('added_terms')]
        
        return {
            'total_queries': total,
            'expanded_queries': expanded,
            'expansion_rate': expansion_rate,
            'top_added_terms': term_counter.most_common(10),
            'no_expansion_queries': no_expansion[:20]  # primeiras 20
        }
    
    def analyze_votes(self) -> Dict:
        """Analisa padrões de votos (👍/👎)."""
        thumbs_up = sum(1 for v in self.votes if v.get('vote') == 'up')
        thumbs_down = sum(1 for v in self.votes if v.get('vote') == 'down')
        total_votes = len(self.votes)
        
        satisfaction_rate = (thumbs_up / total_votes * 100) if total_votes > 0 else 0
        
        # Queries com mais votos negativos
        down_votes_by_query = defaultdict(int)
        for v in self.votes:
            if v.get('vote') == 'down':
                query = v.get('question', '')[:100]  # primeiros 100 chars
                down_votes_by_query[query] += 1
        
        # Documentos com mais votos negativos
        down_votes_by_doc = defaultdict(int)
        for v in self.votes:
            if v.get('vote') == 'down':
                for doc_id in v.get('doc_ids', []):
                    down_votes_by_doc[doc_id] += 1
        
        return {
            'total_votes': total_votes,
            'thumbs_up': thumbs_up,
            'thumbs_down': thumbs_down,
            'satisfaction_rate': satisfaction_rate,
            'worst_queries': sorted(down_votes_by_query.items(), key=lambda x: x[1], reverse=True)[:10],
            'worst_documents': sorted(down_votes_by_doc.items(), key=lambda x: x[1], reverse=True)[:10]
        }
    
    def analyze_search_patterns(self) -> Dict:
        """Analisa padrões de busca."""
        search_types = Counter(q.get('search_type', 'unknown') for q in self.queries)
        
        # Queries mais comuns (normalizadas)
        normalized_queries = []
        for q in self.queries:
            original = q.get('original_query', '').lower()
            tokens = original.split()
            normalized = ' '.join(normalize_token(t) for t in tokens)
            normalized_queries.append(normalized)
        
        query_counter = Counter(normalized_queries)
        
        # Análise de resultados
        avg_results = sum(q.get('num_results', 0) for q in self.queries) / len(self.queries) if self.queries else 0
        
        return {
            'search_types': dict(search_types),
            'top_queries': query_counter.most_common(15),
            'avg_results': avg_results
        }
    
    def analyze_guardrails(self) -> Dict:
        """Analisa violações de guardrails."""
        total_violations = len(self.guardrail_violations)
        
        # Separar por tipo
        input_violations = [v for v in self.guardrail_violations if v.get('type') == 'input_violation']
        output_violations = [v for v in self.guardrail_violations if v.get('type') == 'output_violation']
        
        # Contar por tipo de violação (input)
        violation_types = Counter()
        for v in input_violations:
            for violation in v.get('violations', []):
                violation_types[violation['type']] += 1
        
        # Contar por severity
        severity_counter = Counter()
        for v in input_violations:
            for violation in v.get('violations', []):
                severity_counter[violation['severity']] += 1
        
        # Output violation types
        output_violation_types = Counter(v.get('violation_type', 'unknown') for v in output_violations)
        
        # Perguntas mais bloqueadas
        blocked_questions = Counter()
        for v in input_violations:
            q = v.get('question', '')[:100]
            if q:
                blocked_questions[q] += 1
        
        return {
            'total_violations': total_violations,
            'input_violations': len(input_violations),
            'output_violations': len(output_violations),
            'violation_types': dict(violation_types.most_common(10)),
            'severity_distribution': dict(severity_counter),
            'output_violation_types': dict(output_violation_types),
            'top_blocked_questions': blocked_questions.most_common(10)
        }
    
    def identify_missing_terms(self) -> List[Tuple[str, int]]:
        """Identifica termos que aparecem frequentemente mas não expandem."""
        # Extrair termos de queries que NÃO expandiram
        no_expansion_terms = []
        for q in self.queries:
            if not q.get('added_terms'):
                original = q.get('original_query', '').lower()
                tokens = original.split()
                for token in tokens:
                    # Normalizar e filtrar stopwords
                    normalized = normalize_token(token)
                    if len(normalized) > 3 and normalized not in ['qual', 'como', 'quai', 'onde', 'quando', 'porque']:
                        no_expansion_terms.append(normalized)
        
        term_counter = Counter(no_expansion_terms)
        return term_counter.most_common(20)
    
    def generate_report(self, output_path: str = "data/telemetry_report.html"):
        """Gera relatório HTML com todas as análises."""
        expansion = self.analyze_query_expansion()
        votes = self.analyze_votes()
        patterns = self.analyze_search_patterns()
        missing = self.identify_missing_terms()
        guardrails = self.analyze_guardrails()  # Nova análise
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório de Telemetria - IAmiga</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 15px; }}
        .metric {{ display: inline-block; background: #ecf0f1; padding: 15px 25px; margin: 10px; border-radius: 5px; min-width: 150px; }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #3498db; }}
        .metric-label {{ font-size: 14px; color: #7f8c8d; margin-top: 5px; }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #f39c12; }}
        .danger {{ color: #e74c3c; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }}
        .badge-success {{ background: #27ae60; color: white; }}
        .badge-warning {{ background: #f39c12; color: white; }}
        .badge-danger {{ background: #e74c3c; color: white; }}
        .timestamp {{ text-align: right; color: #95a5a6; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Relatório de Telemetria - IAmiga</h1>
        <p>Análise completa do sistema de Query Rewrite + Re-ranking</p>
        
        <h2>📈 Métricas Gerais</h2>
        <div>
            <div class="metric">
                <div class="metric-value">{len(self.events)}</div>
                <div class="metric-label">Total de Eventos</div>
            </div>
            <div class="metric">
                <div class="metric-value">{expansion['total_queries']}</div>
                <div class="metric-label">Queries Processadas</div>
            </div>
            <div class="metric">
                <div class="metric-value">{votes['total_votes']}</div>
                <div class="metric-label">Votos Recebidos</div>
            </div>
        </div>
        
        <h2>🔄 Expansão de Queries</h2>
        <div>
            <div class="metric">
                <div class="metric-value {'success' if expansion['expansion_rate'] > 50 else 'warning'}">{expansion['expansion_rate']:.1f}%</div>
                <div class="metric-label">Taxa de Expansão</div>
            </div>
            <div class="metric">
                <div class="metric-value">{expansion['expanded_queries']}</div>
                <div class="metric-label">Queries Expandidas</div>
            </div>
        </div>
        
        <h3>Top 10 Termos Adicionados</h3>
        <table>
            <tr><th>Termo</th><th>Frequência</th></tr>
"""
        for term, count in expansion['top_added_terms']:
            html += f"            <tr><td>{term}</td><td>{count}</td></tr>\n"
        
        html += f"""        </table>
        
        <h2>👍👎 Análise de Votos</h2>
        <div>
            <div class="metric">
                <div class="metric-value {'success' if votes['satisfaction_rate'] > 70 else 'danger'}">{votes['satisfaction_rate']:.1f}%</div>
                <div class="metric-label">Taxa de Satisfação</div>
            </div>
            <div class="metric">
                <div class="metric-value success">{votes['thumbs_up']}</div>
                <div class="metric-label">👍 Positivos</div>
            </div>
            <div class="metric">
                <div class="metric-value danger">{votes['thumbs_down']}</div>
                <div class="metric-label">👎 Negativos</div>
            </div>
        </div>
        
        <h3>Queries com Mais Votos Negativos (precisam atenção!)</h3>
        <table>
            <tr><th>Query</th><th>Votos 👎</th></tr>
"""
        for query, count in votes['worst_queries']:
            html += f"            <tr><td>{query[:80]}...</td><td><span class='badge badge-danger'>{count}</span></td></tr>\n"
        
        html += """        </table>
        
        <h3>Documentos com Mais Votos Negativos (revisar relevância!)</h3>
        <table>
            <tr><th>Documento ID</th><th>Votos 👎</th></tr>
"""
        for doc_id, count in votes['worst_documents']:
            html += f"            <tr><td>{doc_id}</td><td><span class='badge badge-danger'>{count}</span></td></tr>\n"
        
        html += f"""        </table>
        
        <h2>🔍 Padrões de Busca</h2>
        <div>
            <div class="metric">
                <div class="metric-value">{patterns['avg_results']:.1f}</div>
                <div class="metric-label">Média de Resultados</div>
            </div>
        </div>
        
        <h3>Top 15 Queries Mais Frequentes</h3>
        <table>
            <tr><th>Query (normalizada)</th><th>Frequência</th></tr>
"""
        for query, count in patterns['top_queries']:
            html += f"            <tr><td>{query[:100]}</td><td>{count}</td></tr>\n"
        
        # SEÇÃO GUARDRAILS
        html += f"""        </table>
        
        <h2>🛡️ Guardrails - Segurança e Proteção</h2>
        <div>
            <div class="metric">
                <div class="metric-value {'warning' if guardrails['total_violations'] > 0 else 'success'}">{guardrails['total_violations']}</div>
                <div class="metric-label">Total de Violações</div>
            </div>
            <div class="metric">
                <div class="metric-value danger">{guardrails['input_violations']}</div>
                <div class="metric-label">🛡️ Entradas Bloqueadas</div>
            </div>
            <div class="metric">
                <div class="metric-value warning">{guardrails['output_violations']}</div>
                <div class="metric-label">🚫 Saídas Filtradas</div>
            </div>
        </div>
        
        <h3>Tipos de Violações de Entrada</h3>
        <table>
            <tr><th>Tipo</th><th>Frequência</th><th>Ação</th></tr>
"""
        for vtype, count in guardrails['violation_types'].items():
            html += f"            <tr><td>{vtype}</td><td>{count}</td><td><span class='badge badge-danger'>BLOQUEADO</span></td></tr>\n"
        
        html += f"""        </table>
        
        <h3>Distribuição por Severidade</h3>
        <table>
            <tr><th>Severidade</th><th>Ocorrências</th></tr>
"""
        for severity, count in guardrails['severity_distribution'].items():
            badge_class = 'badge-danger' if severity == 'critical' else ('badge-warning' if severity == 'high' else 'badge-success')
            html += f"            <tr><td><span class='badge {badge_class}'>{severity.upper()}</span></td><td>{count}</td></tr>\n"
        
        if guardrails['top_blocked_questions']:
            html += f"""        </table>
        
        <h3>Perguntas Mais Bloqueadas (Top 10)</h3>
        <table>
            <tr><th>Pergunta</th><th>Bloqueios</th></tr>
"""
            for question, count in guardrails['top_blocked_questions']:
                html += f"            <tr><td>{question}</td><td><span class='badge badge-danger'>{count}</span></td></tr>\n"
        
        html += """        </table>
        
        <h2>⚠️ Termos Candidatos para Glossário</h2>
        <p>Termos que aparecem frequentemente em queries SEM expansão (podem precisar de aliases):</p>
        <table>
            <tr><th>Termo</th><th>Frequência</th><th>Sugestão</th></tr>
"""
        for term, count in missing:
            badge_class = 'badge-danger' if count > 5 else 'badge-warning' if count > 2 else 'badge-success'
            html += f"            <tr><td><strong>{term}</strong></td><td><span class='badge {badge_class}'>{count}</span></td><td>Adicionar ao glossário?</td></tr>\n"
        
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html += f"""        </table>
        
        <div class="timestamp">
            Relatório gerado em: {timestamp}
        </div>
    </div>
</body>
</html>
"""
        
        output_file = Path(output_path)
        output_file.write_text(html, encoding='utf-8')
        return str(output_file.absolute())


def main():
    print("=" * 80)
    print("ANÁLISE DE TELEMETRIA - IAmiga")
    print("=" * 80)
    
    analyzer = TelemetryAnalyzer()
    analyzer.load_data()
    
    if not analyzer.events:
        print("\n[!] Nenhum evento encontrado. Execute algumas queries primeiro!")
        return
    
    print("\n[*] Analisando expansão de queries...")
    expansion = analyzer.analyze_query_expansion()
    print(f"   Taxa de expansão: {expansion['expansion_rate']:.1f}%")
    print(f"   Queries expandidas: {expansion['expanded_queries']}/{expansion['total_queries']}")
    
    print("\n[*] Analisando votos...")
    votes = analyzer.analyze_votes()
    if votes['total_votes'] > 0:
        print(f"   Satisfação: {votes['satisfaction_rate']:.1f}%")
        print(f"   Positivos: {votes['thumbs_up']} | Negativos: {votes['thumbs_down']}")
    else:
        print("   Nenhum voto registrado ainda")
    
    print("\n[*] Analisando padrões de busca...")
    patterns = analyzer.analyze_search_patterns()
    print(f"   Média de resultados: {patterns['avg_results']:.1f}")
    
    print("\n[*] Identificando termos candidatos ao glossário...")
    missing = analyzer.identify_missing_terms()
    if missing:
        print(f"   Encontrados {len(missing)} termos candidatos")
        print("   Top 5:", [t[0] for t in missing[:5]])
    
    print("\n[*] Gerando relatório HTML...")
    report_path = analyzer.generate_report()
    
    print("\n" + "=" * 80)
    print("[OK] Análise concluída!")
    print(f"[>>] Relatório: {report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
