# check_stats.py
import json

with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'📊 Total de entradas: {len(data)}')
print(f'📁 Tipos: {set(item["type"] for item in data)}')
print(f'📄 Fontes: {set(item["source"] for item in data)}')

# Detalhes por fonte
print('\n📈 Detalhes por arquivo:')
from collections import Counter
sources = Counter(item["source"] for item in data)
for source, count in sources.items():
    print(f'  {source}: {count} entradas')

# Tamanho médio dos conteúdos
lengths = [item["length"] for item in data]
avg_length = sum(lengths) / len(lengths) if lengths else 0
print(f'\n📏 Tamanho médio do conteúdo: {avg_length:.0f} caracteres')