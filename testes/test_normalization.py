# test_normalization.py
"""Testa a normalização morfológica (singular/plural + diacríticos)"""
import sys
from pathlib import Path

# Adicionar src/ ao path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from core.search.query_rewriter import strip_accents, singularize_pt, normalize_token, QueryRewriter

print("=" * 80)
print("TESTE: Normalização Morfológica")
print("=" * 80)

# Teste 1: Remoção de acentos
print("\n📝 Teste 1: Remoção de diacríticos")
print("-" * 80)
test_cases_accents = [
    ("operação", "operacao"),
    ("crédito", "credito"),
    ("condições", "condicoes"),
    ("préstamo", "prestamo"),
    ("Açúcar", "acucar"),
]

for word, expected in test_cases_accents:
    result = strip_accents(word)
    status = "✅" if result == expected else "❌"
    print(f"{status} '{word}' → '{result}' (esperado: '{expected}')")

# Teste 2: Singularização
print("\n📝 Teste 2: Singularização em português")
print("-" * 80)
test_cases_singular = [
    ("operações", "operacao"),  # ções → ção
    ("condições", "condicao"),  # ções → ção
    ("operacoes", "operacao"),  # ões → ão (sem acento)
    ("pães", "pao"),            # ães → ão
    ("contratos", "contrato"),  # s final
    ("clientes", "cliente"),    # s final
    ("empréstimos", "emprestimo"),  # s final
]

for word, expected in test_cases_singular:
    result = singularize_pt(word)
    status = "✅" if result == expected.lower() else "❌"
    print(f"{status} '{word}' → '{result}' (esperado: '{expected}')")

# Teste 3: Normalização completa (acentos + singular)
print("\n📝 Teste 3: Normalização completa (strip_accents + singularize)")
print("-" * 80)
test_cases_normalize = [
    ("operações", "operacao"),
    ("condições", "condicao"),
    ("contratos", "contrato"),
    ("empréstimos", "emprestimo"),
    ("créditos", "credito"),
    ("pães", "pao"),
]

for word, expected in test_cases_normalize:
    result = normalize_token(word)
    status = "✅" if result == expected else "❌"
    print(f"{status} '{word}' → '{result}' (esperado: '{expected}')")

# Teste 4: Query Rewrite com normalização
print("\n📝 Teste 4: Query Rewrite com normalização morfológica")
print("-" * 80)

rewriter = QueryRewriter(glossario_path="src/core/domain/glossario.json")

test_queries = [
    "Quais os tipos de operações do Crediamigo?",  # plural com acento
    "Qual o prazo das condições de pagamento?",    # plural com acento
    "Como funcionam os empréstimos?",              # plural com acento
    "Preciso de informações sobre contratos",      # plural sem acento
]

for query in test_queries:
    expanded, added = rewriter.rewrite(query)
    print(f"\n🔍 Query: '{query}'")
    print(f"   ↳ Expandida: '{expanded}'")
    print(f"   ↳ Termos adicionados: {added}")

print("\n" + "=" * 80)
print("✅ Testes de normalização concluídos!")
print("=" * 80)
