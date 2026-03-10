import json

# Carregar knowledge base
with open('data/knowledge_base.json', encoding='utf-8') as f:
    kb = json.load(f)

# Procurar no E-BOOK01
ebook = [d for d in kb if 'E-BOOK01' in d['source']]
print(f'Total chunks E-BOOK01: {len(ebook)}\n')

# Procurar chunks que mencionam essas palavras
keywords = ['seguro vida', 'seguro prestamista', 'maquininha', 'soluções digitais']

for keyword in keywords:
    chunks = [d for d in ebook if keyword.lower() in d['content'].lower()]
    if chunks:
        print(f'\n{"="*80}')
        print(f'Keyword: "{keyword}" - {len(chunks)} chunks encontrados')
        print(f'{"="*80}')
        for i, chunk in enumerate(chunks[:2], 1):
            print(f'\nChunk {i}:')
            print(chunk['content'][:400])
