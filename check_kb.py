import json

# Carregar knowledge base
with open('data/knowledge_base.json', encoding='utf-8') as f:
    kb = json.load(f)

# Procurar documentos sobre linhas de crédito
linhas = [d for d in kb if 'linha' in d['content'].lower() and 'crédito' in d['content'].lower()]

print(f'Total documentos com "linha" + "crédito": {len(linhas)}')
print('\nTop 10 documentos:')
for i, d in enumerate(linhas[:10], 1):
    print(f"\n{i}. {d['source']}")
    print(f"   Tipo: {d.get('kind', 'N/A')}")
    print(f"   Conteudo: {d['content'][:150]}...")

# Procurar especificamente o documento de linhas de crédito
doc_linhas = [d for d in kb if '1102-05-01' in d['source']]
print(f"\n\nDocumentos '1102-05-01 - Linhas de Crédito': {len(doc_linhas)}")
for i, d in enumerate(doc_linhas[:3], 1):
    print(f"\n{i}. ID: {d['id']}")
    print(f"   Content: {d['content'][:200]}...")
