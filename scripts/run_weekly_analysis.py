#!/usr/bin/env python3
# scripts/run_weekly_analysis.py
"""
Script integrado para execução semanal/mensal.
Combina análise de telemetria + sugestões de glossário.
"""

import sys
from pathlib import Path
import webbrowser

# Adicionar scripts ao path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from analyze_telemetry import TelemetryAnalyzer
from suggest_glossary_updates import GlossarySuggester


def main():
    print("=" * 80)
    print("🤖 ANÁLISE SEMANAL AUTOMÁTICA - IAmiga RAG System")
    print("=" * 80)
    
    # 1. Análise de Telemetria
    print("\n📊 ETAPA 1/2: Análise de Telemetria")
    print("-" * 80)
    
    analyzer = TelemetryAnalyzer()
    analyzer.load_data()
    
    if not analyzer.events:
        print("\n⚠️  Nenhum dado de telemetria encontrado!")
        print("Execute algumas queries no sistema antes de rodar esta análise.")
        return
    
    html_report = analyzer.generate_report()
    
    # 2. Sugestões de Glossário
    print("\n🔍 ETAPA 2/2: Sugestões de Glossário")
    print("-" * 80)
    
    suggester = GlossarySuggester()
    suggester.load_telemetry()
    md_report = suggester.generate_suggestions_report()
    
    # Resumo Final
    print("\n" + "=" * 80)
    print("✅ ANÁLISE COMPLETA!")
    print("=" * 80)
    
    expansion = analyzer.analyze_query_expansion()
    votes = analyzer.analyze_votes()
    
    print(f"\n📈 MÉTRICAS PRINCIPAIS:")
    print(f"   • Total de eventos: {len(analyzer.events)}")
    print(f"   • Queries processadas: {expansion['total_queries']}")
    print(f"   • Taxa de expansão: {expansion['expansion_rate']:.1f}%")
    
    if votes['total_votes'] > 0:
        print(f"   • Taxa de satisfação: {votes['satisfaction_rate']:.1f}%")
        print(f"   • Votos: 👍 {votes['thumbs_up']} | 👎 {votes['thumbs_down']}")
    
    print(f"\n📂 RELATÓRIOS GERADOS:")
    print(f"   1. HTML Dashboard: {html_report}")
    print(f"   2. Sugestões MD: {md_report}")
    
    print(f"\n💡 PRÓXIMOS PASSOS:")
    print(f"   1. Abra o dashboard HTML no navegador")
    print(f"   2. Revise as sugestões de glossário (MD)")
    print(f"   3. Aplique mudanças em src/core/domain/glossario.json")
    print(f"   4. Reinicie o sistema e monitore por 1 semana")
    
    print("\n" + "=" * 80)
    
    # Perguntar se deseja abrir o relatório HTML
    try:
        response = input("\n🌐 Abrir relatório HTML no navegador? (s/n): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            webbrowser.open(f'file:///{html_report}')
            print("✅ Relatório aberto!")
    except:
        pass


if __name__ == "__main__":
    main()
