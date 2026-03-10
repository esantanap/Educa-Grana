"""
Counterfactual Explanations para RAG
Gera explicações do tipo "se você tivesse perguntado X, a resposta seria..."
"""

import re
from typing import List, Dict, Any, Tuple
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.search.query_rewriter import QueryRewriter


class CounterfactualGenerator:
    """Gerador de explicações contrafactuais para queries RAG."""
    
    def __init__(self):
        # Não precisamos do QueryRewriter para counterfactuals
        # As sugestões são baseadas em heurísticas simples
        pass
    
    def generate_counterfactuals(
        self,
        original_query: str,
        num_results: int,
        added_terms: List[str]
    ) -> List[Dict[str, Any]]:
        """Gera explicações contrafactuais baseadas na query.
        
        Args:
            original_query: Query original do usuário
            num_results: Número de resultados obtidos
            added_terms: Termos adicionados pela expansão
            
        Returns:
            Lista de counterfactuals com tipo e mensagem
        """
        counterfactuals = []
        
        # 1. Counterfactual: Se não tivesse expandido
        if added_terms:
            counterfactuals.append({
                'type': 'no_expansion',
                'original': original_query,
                'variation': self._remove_expansion_terms(original_query, added_terms),
                'message': f'Se não expandisse a query (sem sinônimos), provavelmente teria menos resultados ou menos precisos.',
                'impact': 'negative',
                'terms_affected': added_terms
            })
        
        # 2. Counterfactual: Se adicionasse termos mais específicos
        specific_terms = self._suggest_specific_terms(original_query)
        if specific_terms:
            counterfactuals.append({
                'type': 'more_specific',
                'original': original_query,
                'variation': f"{original_query} {specific_terms}",
                'message': f'Adicionar "{specific_terms}" tornaria a busca mais específica e focada.',
                'impact': 'positive',
                'suggested_terms': specific_terms
            })
        
        # 3. Counterfactual: Se removesse termos vagos
        vague_terms = self._identify_vague_terms(original_query)
        if vague_terms:
            simplified = self._remove_terms(original_query, vague_terms)
            counterfactuals.append({
                'type': 'remove_vague',
                'original': original_query,
                'variation': simplified,
                'message': f'Remover termos vagos como "{vague_terms[0]}" focaria melhor a busca.',
                'impact': 'neutral',
                'removed_terms': vague_terms
            })
        
        # 4. Counterfactual: Se mudasse o foco da pergunta
        alternative_focus = self._suggest_alternative_focus(original_query)
        if alternative_focus:
            counterfactuals.append({
                'type': 'alternative_focus',
                'original': original_query,
                'variation': alternative_focus['query'],
                'message': alternative_focus['message'],
                'impact': 'alternative',
                'focus': alternative_focus['focus']
            })
        
        # 5. Counterfactual: Resultado baseado em performance
        if num_results < 3:
            counterfactuals.append({
                'type': 'low_results',
                'original': original_query,
                'variation': self._broaden_query(original_query),
                'message': 'Como foram encontrados poucos resultados, uma query mais ampla poderia ajudar.',
                'impact': 'positive',
                'reason': 'low_results'
            })
        elif num_results > 10:
            counterfactuals.append({
                'type': 'too_many_results',
                'original': original_query,
                'variation': self._narrow_query(original_query),
                'message': 'Muitos resultados foram encontrados. Uma query mais específica seria mais precisa.',
                'impact': 'positive',
                'reason': 'high_results'
            })
        
        return counterfactuals
    
    def _remove_expansion_terms(self, query: str, added_terms: List[str]) -> str:
        """Remove termos de expansão da query."""
        result = query
        for term in added_terms:
            result = result.replace(term, '').strip()
        # Limpar espaços duplos
        result = re.sub(r'\s+', ' ', result)
        return result
    
    def _suggest_specific_terms(self, query: str) -> str:
        """Sugere termos mais específicos baseado no contexto."""
        query_lower = query.lower()
        
        suggestions = {
            'empréstimo': 'documentos necessários',
            'crédito': 'taxa de juros',
            'financiamento': 'prazo',
            'cliente': 'requisitos',
            'valor': 'limite máximo',
            'parcela': 'quantidade de parcelas',
            'juros': 'taxa mensal',
            'Educa Grana': 'linhas disponíveis'
        }
        
        for key, suggestion in suggestions.items():
            if key in query_lower and suggestion not in query_lower:
                return suggestion
        
        return ""
    
    def _identify_vague_terms(self, query: str) -> List[str]:
        """Identifica termos vagos na query."""
        vague_words = [
            'como', 'qual', 'quanto', 'onde', 'quando', 'quem',
            'pode', 'consigo', 'existe', 'tem', 'há'
        ]
        
        query_words = query.lower().split()
        found_vague = [word for word in vague_words if word in query_words]
        
        return found_vague[:2]  # Retornar no máximo 2
    
    def _remove_terms(self, query: str, terms: List[str]) -> str:
        """Remove termos específicos da query."""
        result = query
        for term in terms:
            # Remover palavra completa (case insensitive)
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            result = pattern.sub('', result)
        
        # Limpar espaços e pontuação duplicada
        result = re.sub(r'\s+', ' ', result).strip()
        result = re.sub(r'\?\s*\?', '?', result)
        
        return result
    
    def _suggest_alternative_focus(self, query: str) -> Dict[str, str]:
        """Sugere foco alternativo para a query."""
        query_lower = query.lower()
        
        # Mapear tópicos para alternativas
        alternatives = {
            'documentos': {
                'focus': 'processo',
                'query': 'qual o processo de aprovação?',
                'message': 'Em vez de focar em documentos, você poderia perguntar sobre o processo de aprovação.'
            },
            'valor': {
                'focus': 'elegibilidade',
                'query': 'quem pode solicitar?',
                'message': 'Além do valor, seria útil saber sobre elegibilidade para o crédito.'
            },
            'taxa': {
                'focus': 'prazo',
                'query': 'qual o prazo de pagamento?',
                'message': 'Além da taxa, considere perguntar sobre prazos de pagamento disponíveis.'
            }
        }
        
        for keyword, alternative in alternatives.items():
            if keyword in query_lower:
                return alternative
        
        return {}
    
    def _broaden_query(self, query: str) -> str:
        """Amplia a query removendo especificidades."""
        # Remover números e especificações
        broader = re.sub(r'\b\d+\b', '', query)
        broader = re.sub(r'\bespecífico\b|\bexato\b|\bpreciso\b', '', broader, flags=re.IGNORECASE)
        broader = re.sub(r'\s+', ' ', broader).strip()
        
        # Se ficou muito curta, adicionar termo genérico
        if len(broader.split()) < 3:
            broader = f"informações sobre {broader}"
        
        return broader
    
    def _narrow_query(self, query: str) -> str:
        """Torna a query mais específica."""
        query_lower = query.lower()
        
        # Adicionar qualificadores específicos
        if 'Educa Grana' in query_lower and 'linha' not in query_lower:
            return f"{query} linhas específicas"
        elif 'empréstimo' in query_lower and 'tipo' not in query_lower:
            return f"{query} tipos disponíveis"
        elif 'crédito' in query_lower and 'modalidade' not in query_lower:
            return f"{query} modalidades"
        else:
            return f"{query} detalhes específicos"
    
    def format_counterfactual_message(self, counterfactual: Dict[str, Any]) -> str:
        """Formata counterfactual para exibição amigável."""
        impact_emoji = {
            'positive': '✅',
            'negative': '❌',
            'neutral': '➡️',
            'alternative': '🔄'
        }
        
        emoji = impact_emoji.get(counterfactual.get('impact', 'neutral'), '💡')
        
        msg = f"{emoji} **{counterfactual['message']}**\n\n"
        msg += f"📝 **Original:** {counterfactual['original']}\n"
        msg += f"🔀 **Variação:** {counterfactual['variation']}"
        
        return msg


# Instância global
counterfactual_generator = CounterfactualGenerator()
