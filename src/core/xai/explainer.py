"""
Módulo XAI (Explainable AI) para rastreamento de decisões.
Registra explicações sobre como o sistema processa queries e gera respostas.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class XAILogger:
    """Logger para explicações de IA."""
    
    def __init__(self, log_path: str = "data/xai_explanations.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _write_entry(self, entry: Dict[str, Any]) -> None:
        """Escreve entrada no log."""
        try:
            entry['timestamp'] = datetime.now().isoformat()
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Erro ao escrever XAI log: {e}")
    
    def log_query_rewrite(
        self,
        original_query: str,
        rewritten_query: str,
        added_terms: List[str],
        explanation: str = ""
    ) -> None:
        """Registra explicação de reescrita de query."""
        entry = {
            'type': 'query_rewrite',
            'original_query': original_query,
            'rewritten_query': rewritten_query,
            'added_terms': added_terms,
            'expansion_count': len(added_terms),
            'explanation': explanation or f"Expandida com {len(added_terms)} termos sinônimos"
        }
        self._write_entry(entry)
    
    def log_document_retrieval(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        total_docs: int,
        explanation: str = ""
    ) -> None:
        """Registra explicação de recuperação de documentos."""
        # Extrair informações dos docs
        doc_info = []
        for doc in retrieved_docs[:10]:  # Top 10
            doc_info.append({
                'score': doc.get('score', 0),
                'snippet': doc.get('page_content', '')[:200],
                'matched_terms': doc.get('matched_terms', [])
            })
        
        entry = {
            'type': 'document_retrieval',
            'query': query,
            'retrieved_docs': doc_info,
            'total_retrieved': len(retrieved_docs),
            'total_available': total_docs,
            'explanation': explanation or f"Recuperados {len(retrieved_docs)} de {total_docs} documentos disponíveis"
        }
        self._write_entry(entry)
    
    def log_confidence_score(
        self,
        confidence: float,
        factors: Dict[str, Any],
        explanation: str = ""
    ) -> None:
        """Registra explicação de confidence score."""
        entry = {
            'type': 'confidence_score',
            'confidence': confidence,
            'factors': factors,
            'explanation': explanation or self._generate_confidence_explanation(confidence, factors)
        }
        self._write_entry(entry)
    
    def _generate_confidence_explanation(self, confidence: float, factors: Dict[str, Any]) -> str:
        """Gera explicação textual do confidence score."""
        if confidence >= 0.8:
            level = "alta"
        elif confidence >= 0.6:
            level = "média"
        else:
            level = "baixa"
        
        explanations = [f"Confiança {level} ({confidence*100:.1f}%)"]
        
        if 'doc_scores' in factors:
            avg_score = factors['doc_scores']
            explanations.append(f"Score médio dos documentos: {avg_score:.3f}")
        
        if 'coverage' in factors:
            coverage = factors['coverage']
            explanations.append(f"Cobertura da query: {coverage*100:.1f}%")
        
        return ". ".join(explanations)
    
    def log_citation(
        self,
        citations: List[Dict[str, str]],
        explanation: str = ""
    ) -> None:
        """Registra explicação de citações."""
        entry = {
            'type': 'citation',
            'citations': citations,
            'total_citations': len(citations),
            'explanation': explanation or f"{len(citations)} fontes citadas na resposta"
        }
        self._write_entry(entry)
    
    def log_guardrails(
        self,
        passed: bool,
        violations: List[Dict[str, str]],
        query: str = "",
        explanation: str = ""
    ) -> None:
        """Registra explicação de guardrails."""
        entry = {
            'type': 'guardrails',
            'passed': passed,
            'violations': violations,
            'query_snippet': query[:100] if query else "",
            'total_violations': len(violations),
            'explanation': explanation or self._generate_guardrails_explanation(passed, violations)
        }
        self._write_entry(entry)
    
    def _generate_guardrails_explanation(self, passed: bool, violations: List[Dict[str, str]]) -> str:
        """Gera explicação textual dos guardrails."""
        if passed:
            return "Query passou em todas as validações de segurança"
        else:
            critical = len([v for v in violations if v.get('severity') == 'critical'])
            if critical > 0:
                return f"Query bloqueada: {critical} violação(ões) crítica(s) detectada(s)"
            else:
                return f"Query bloqueada: {len(violations)} violação(ões) detectada(s)"
    
    def log_reranking(
        self,
        original_scores: List[float],
        reranked_scores: List[float],
        explanation: str = ""
    ) -> None:
        """Registra explicação de re-ranking."""
        entry = {
            'type': 'reranking',
            'original_scores': original_scores[:10],
            'reranked_scores': reranked_scores[:10],
            'improvement': self._calculate_ranking_improvement(original_scores, reranked_scores),
            'explanation': explanation or "Documentos re-ordenados para melhor relevância"
        }
        self._write_entry(entry)
    
    def _calculate_ranking_improvement(self, original: List[float], reranked: List[float]) -> float:
        """Calcula melhoria no ranking."""
        if not original or not reranked:
            return 0.0
        
        # Calcula diferença média nos top-k scores
        k = min(5, len(original), len(reranked))
        orig_avg = sum(original[:k]) / k
        rerank_avg = sum(reranked[:k]) / k
        
        return rerank_avg - orig_avg
    
    def log_counterfactual(
        self,
        counterfactuals: List[Dict[str, Any]],
        query: str,
        explanation: str = ""
    ) -> None:
        """Registra explicações contrafactuais."""
        entry = {
            'type': 'counterfactual',
            'query': query,
            'counterfactuals': counterfactuals,
            'total_counterfactuals': len(counterfactuals),
            'explanation': explanation or f"{len(counterfactuals)} cenários alternativos gerados"
        }
        self._write_entry(entry)


# Instância global
xai_logger = XAILogger()
