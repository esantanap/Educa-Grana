#src/core/guardrails/output_filter.py
import re
from typing import Tuple, List

class OutputGuardrails:
    """Guardrails para validar respostas antes de enviar ao usuário."""
    
    def __init__(self):
        # Padrões que não devem aparecer nas respostas
        self.forbidden_response_patterns = [
            # Informações do sistema (mais específicas para evitar falsos positivos)
            r"como modelo de linguagem|sou uma ia treinada|sou um assistente virtual treinado",
            r"sou uma ia|sou um modelo de",
            r"desculpe, mas não posso ajudar com isso",
            
            # Informações técnicas que não devem vazar
            r"langchain|chromadb|openai api",
            r"embedding vector|vector database|chroma",
            r"system prompt|instruções do sistema",
            
            # Informações sensíveis que podem ter passado
            r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",  # CPF
            r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",  # CNPJ
        ]
        
        # Disclaimers obrigatórios para certos tipos de resposta
        self.disclaimers = {
            'financial_advice': """
⚠️ **Aviso:** Esta informação é apenas orientativa. Para decisões financeiras importantes, consulte um especialista do BNB.""",
            
            'legal_advice': """
⚠️ **Aviso:** Esta informação não constitui aconselhamento jurídico. Consulte o departamento jurídico para questões legais.""",
            
            'policy_info': """
📋 **Nota:** Políticas podem ser atualizadas. Verifique sempre a versão mais recente nos canais oficiais."""
        }
    
    def _log_violation(self, question: str, response: str, violation_type: str) -> None:
        """Registrar violação de saída em arquivo de log."""
        import json
        from datetime import datetime
        from pathlib import Path
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            log_file = Path(__file__).parent.parent.parent.parent / "data" / "guardrails.log"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "output_violation",
                "question": question[:200],
                "response_preview": response[:200],
                "violation_type": violation_type,
                "severity": "high"
            }
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.debug(f"Erro ao gravar log de violação: {e}")
    
    def validate_response(self, response: str, question: str) -> Tuple[bool, str]:
        """
        Valida resposta antes de enviar ao usuário.
        
        Returns:
            Tuple[bool, str]: (is_valid, processed_response)
        """
        # 1. Verificar padrões proibidos
        if self._contains_forbidden_patterns(response):
            self._log_violation(question, response, "forbidden_pattern")
            return False, self._get_safe_fallback_response()
        
        # 2. Limpar informações sensíveis que podem ter vazado
        cleaned_response = self._clean_response(response)
        
        # 3. Adicionar disclaimers apropriados
        final_response = self._add_disclaimers(cleaned_response, question)
        
        # 4. Verificar qualidade da resposta
        if self._is_low_quality_response(final_response):
            return False, self._get_safe_fallback_response()
        
        return True, final_response
    
    def _contains_forbidden_patterns(self, response: str) -> bool:
        """Verifica se a resposta contém padrões proibidos."""
        response_lower = response.lower()
        
        for pattern in self.forbidden_response_patterns:
            if re.search(pattern, response_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _clean_response(self, response: str) -> str:
        """Remove informações sensíveis da resposta."""
        # Mascarar CPFs que podem ter vazado
        response = re.sub(
            r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',
            '***.***.***-**',
            response
        )
        
        # Mascarar CNPJs
        response = re.sub(
            r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b',
            '**.***.***/****-**',
            response
        )
        
        # Remover referências técnicas
        response = re.sub(
            r'\b(langchain|chromadb|openai|embedding|vector)\b',
            '[sistema]',
            response,
            flags=re.IGNORECASE
        )
        
        return response
    
    def _add_disclaimers(self, response: str, question: str) -> str:
        """Adiciona disclaimers apropriados baseado no tipo de pergunta."""
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Detectar se é conselho financeiro
        financial_keywords = ['investir', 'empréstimo', 'financiamento', 'juros', 'taxa']
        if any(keyword in question_lower for keyword in financial_keywords):
            if 'recomendo' in response_lower or 'sugiro' in response_lower:
                response += "\n\n" + self.disclaimers['financial_advice']
        
        # Detectar se é informação sobre políticas
        policy_keywords = ['política', 'regra', 'norma', 'procedimento']
        if any(keyword in question_lower for keyword in policy_keywords):
            response += "\n\n" + self.disclaimers['policy_info']
        
        # Adicionar assinatura padrão
        response += "\n\n🤖 **IAmiga** - Assistente Virtual do Educa Grana"
        
        return response
    
    def _is_low_quality_response(self, response: str) -> bool:
        """Verifica se a resposta é de baixa qualidade."""
        # Muito curta
        if len(response.strip()) < 20:
            return True
        
        # Apenas disclaimers
        if response.count('⚠️') > 0 and len(response.replace('⚠️', '').strip()) < 50:
            return True
        
        # Resposta genérica demais
        generic_phrases = [
            'não sei', 'não tenho informações', 'não posso ajudar',
            'desculpe', 'não encontrei', 'não há dados'
        ]
        
        if any(phrase in response.lower() for phrase in generic_phrases):
            if len(response) < 100:  # Respostas curtas e genéricas
                return True
        
        return False
    
    def _get_safe_fallback_response(self) -> str:
        """Retorna resposta segura padrão quando a resposta original é rejeitada."""
        return """🤖 **IAmiga aqui!**

Desculpe, não consegui processar sua pergunta adequadamente. 

**Posso ajudar com:**
- 📋 Informações sobre o programa Educa Grana
- 💰 Procedimentos de microcrédito
- 📊 Avaliação de carteira
- 📚 Educação financeira
- 📞 Contatos e canais de atendimento

Tente reformular sua pergunta ou escolha um dos tópicos acima.

🤖 **IAmiga** - Assistente Virtual do Educa Grana"""