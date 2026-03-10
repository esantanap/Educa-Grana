# src/core/search/reranker.py
from __future__ import annotations
from typing import List, Dict, Any

def heuristic_rerank(query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reranker heurístico leve:
    - Boost: termos no título/seção
    - Boost: tipo de documento (normativo/procedimento/fluxo_operacional/apresentacao)
    - Boost: documentos da mesma fonte (agrupa chunks relacionados)
    - Penalização reduzida para chunks fragmentados
    """
    q_terms = set(query.lower().split())

    def score(d: Dict[str, Any]) -> float:
        base = float(d.get("score", 0.0))
        title = (d.get("title") or "").lower()
        section = (d.get("section") or "").lower()
        kind = (d.get("kind") or "oneoff_nota").lower()
        source = (d.get("source") or "").lower()
        length = max(50, min(1500, int(d.get("length", 500))))

        # Boost por termos no título/seção
        hits = len(q_terms.intersection(set(title.split() + section.split())))
        title_boost = 0.05 * hits

        # Boost por tipo de documento (normativos e TABELAS têm prioridade máxima)
        kind_boost = {
            "table": 0.80,  # 🔥 TABELAS TÊM PRIORIDADE MÁXIMA
            "normativo": 0.40,
            "procedimento": 0.30,
            "fluxo_operacional": 0.22,
            "apresentacao": 0.12
        }.get(kind, 0.0)

        # Boost MUITO FORTE para documento específico de linhas de crédito
        source_boost = 0.60 if ("1102-05-01" in source or "linhas de crédito" in source.lower()) else 0.0
        
        # Boost EXTRA se a query menciona "linhas" e o documento é sobre linhas de crédito
        query_match_boost = 0.30 if "linhas" in query.lower() and ("1102-05-01" in source or "linhas de crédito" in source.lower()) else 0.0
        
        # Boost adicional para chunks que contém a tabela de linhas
        content = (d.get("content") or "").lower()
        table_boost = 0.25 if ("capital de giro solidário" in content or "Educa Grana comunidade" in content or "Educa Grana delas" in content) else 0.0

        # Penalização REDUZIDA para chunks muito curtos (aceitar fragmentos de tabelas)
        length_penalty = -0.05 if length < 80 else 0.0

        return base + title_boost + kind_boost + source_boost + query_match_boost + table_boost + length_penalty

    return sorted(docs, key=score, reverse=True)
