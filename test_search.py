import json
from src.agent import LocalSemanticSearchEngine

# Carregar base
with open('data/knowledge_base.json', encoding='utf-8') as f:
    kb = json.load(f)

print(f"Total documentos: {len(kb)}")

# Criar engine
engine = LocalSemanticSearchEngine()
engine.initialize(kb)

# Testar buscas
queries = [
    "quais linhas de credito",
    "linhas de credito disponiveis",
    "tipos de credito crediamigo",
    "capital de giro",
]

for query in queries:
    print(f"\n{'='*80}")
    print(f"Query: '{query}'")
    print(f"{'='*80}")
    
    # Testar com diferentes thresholds
    for threshold in [0.05, 0.10, 0.12, 0.15]:
        results = engine.search(query, top_k=12, min_similarity=threshold)
        print(f"\nThreshold {threshold}: {len(results)} resultados")
        
        if results:
            for i, (score, doc) in enumerate(results[:3], 1):
                print(f"  {i}. Score: {score:.3f} - {doc['source'][:60]}")
