#!/usr/bin/env python
# test_query_rewrite.py - Testar query rewrite e reranking

import sys
from pathlib import Path

# Adicionar src ao path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from agent import answer_question

print("=" * 80)
print("TESTE: Query Rewrite + Reranking")
print("=" * 80)

# Teste 1: Termo 'operação' deve expandir para 'empréstimo', 'contrato', 'ccb'
print("\n📝 Teste 1: 'Qual o prazo máximo de uma operação do Crediamigo?'")
print("-" * 80)
response = answer_question("Qual o prazo máximo de uma operação do Crediamigo?")
print(f"\n✅ Resposta ({len(response)} caracteres):\n")
print(response)

print("\n" + "=" * 80)
print("\n📝 Teste 2: 'Quais tipos de empréstimo existem?'")
print("-" * 80)
response = answer_question("Quais tipos de empréstimo existem?")
print(f"\n✅ Resposta ({len(response)} caracteres):\n")
print(response)

print("\n" + "=" * 80)
print("\n✅ Testes concluídos!")
print("📊 Verifique data/telemetry.log para dados de telemetria")
