# -*- coding: utf-8 -*-
"""
Validador de Persona para IAmiga - Assistente Virtual do Educa Grana.
"""

import re
import logging
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ViolationType(Enum):
    """Tipos de violacoes da persona."""
    MISSING_GREETING = "missing_greeting"
    MISSING_SIGNATURE = "missing_signature"
    FORBIDDEN_CONTENT = "forbidden_content"
    OFF_TOPIC = "off_topic"
    UNPROFESSIONAL_TONE = "unprofessional_tone"
    MISSING_HELP_OFFER = "missing_help_offer"
    TECHNICAL_EXPOSURE = "technical_exposure"

@dataclass
class PersonaViolation:
    """Representa uma violacao das regras da persona."""
    type: ViolationType
    severity: str
    message: str
    suggestion: str
    auto_fixable: bool = False

class PersonaValidator:
    """Validador principal da persona IAmiga."""
    
    def __init__(self):
        self.required_elements = {
            "greeting_words": [
                "ola", "oi", "bom dia", "boa tarde", "boa noite", 
                "seja bem", "bem-vindo", "bem-vinda"
            ],
            "signature_elements": [
                "iamiga", "assistente virtual", "Educa Grana", 
                "banco do nordeste"
            ],
            "help_offers": [
                "posso ajudar", "estou aqui", "como posso", 
                "precisa de", "mais alguma", "outras duvidas"
            ]
        }
        
        self.forbidden_content = {
            "technical_exposure": [
                "eu sou um modelo de linguagem",
                "como ia artificial", "como inteligencia artificial",
                "sou um chatbot", "sou um bot", "sistema de ia"
            ],
            "inappropriate_disclaimers": [
                "nao sou responsavel", "nao posso garantir",
                "consulte um advogado", "procure um especialista"
            ]
        }
        
        self.correction_templates = {
            "add_greeting": "Ola! ",
            "add_signature": "\n\nIAmiga - Assistente Virtual do Educa Grana",
            "add_help_offer": "\n\nPosso ajudar com mais alguma informacao?"
        }
    
    def validate_response(self, response: str, question: str = "") -> Tuple[bool, List[PersonaViolation]]:
        """Valida se a resposta esta alinhada com a persona IAmiga."""
        violations = []
        
        if not response or not isinstance(response, str):
            violations.append(PersonaViolation(
                type=ViolationType.MISSING_SIGNATURE,
                severity="critical",
                message="Resposta vazia ou invalida",
                suggestion="Gerar resposta valida"
            ))
            return False, violations
        
        response_lower = response.lower()
        
        # Verificar elementos obrigatorios
        has_greeting = any(word in response_lower for word in self.required_elements["greeting_words"])
        if not has_greeting and len(response_lower) > 50:
            violations.append(PersonaViolation(
                type=ViolationType.MISSING_GREETING,
                severity="medium",
                message="Resposta nao contem cumprimento adequado",
                suggestion="Adicionar cumprimento caloroso no inicio",
                auto_fixable=True
            ))
        
        has_signature = any(element in response_lower for element in self.required_elements["signature_elements"])
        if not has_signature:
            violations.append(PersonaViolation(
                type=ViolationType.MISSING_SIGNATURE,
                severity="high",
                message="Resposta nao contem identificacao da IAmiga",
                suggestion="Adicionar assinatura da IAmiga",
                auto_fixable=True
            ))
        
        has_help_offer = any(offer in response_lower for offer in self.required_elements["help_offers"])
        if not has_help_offer and len(response_lower) > 100:
            violations.append(PersonaViolation(
                type=ViolationType.MISSING_HELP_OFFER,
                severity="medium",
                message="Resposta nao oferece ajuda adicional",
                suggestion="Adicionar oferta de ajuda no final",
                auto_fixable=True
            ))
        
        # Verificar conteudo proibido
        for tech_phrase in self.forbidden_content["technical_exposure"]:
            if tech_phrase in response_lower:
                violations.append(PersonaViolation(
                    type=ViolationType.TECHNICAL_EXPOSURE,
                    severity="critical",
                    message=f"Exposicao tecnica detectada: '{tech_phrase}'",
                    suggestion="Remover referencias tecnicas e manter foco na persona"
                ))
                break
        
        critical_violations = [v for v in violations if v.severity == 'critical']
        high_violations = [v for v in violations if v.severity == 'high']
        
        is_valid = len(critical_violations) == 0 and len(high_violations) == 0
        
        return is_valid, violations
    
    def auto_fix_response(self, response: str, violations: List[PersonaViolation]) -> str:
        """Aplica correcoes automaticas quando possivel."""
        fixed_response = response
        
        for violation in violations:
            if not violation.auto_fixable:
                continue
                
            if violation.type == ViolationType.MISSING_GREETING:
                if not any(greeting in fixed_response.lower() 
                          for greeting in self.required_elements["greeting_words"]):
                    fixed_response = self.correction_templates["add_greeting"] + fixed_response
            
            elif violation.type == ViolationType.MISSING_SIGNATURE:
                if not any(sig in fixed_response.lower() 
                          for sig in self.required_elements["signature_elements"]):
                    fixed_response += self.correction_templates["add_signature"]
            
            elif violation.type == ViolationType.MISSING_HELP_OFFER:
                if not any(help_word in fixed_response.lower() 
                          for help_word in self.required_elements["help_offers"]):
                    fixed_response += self.correction_templates["add_help_offer"]
        
        return fixed_response

class IAmigaPersona:
    """Classe principal para aplicar a persona IAmiga."""
    
    def __init__(self):
        self.validator = PersonaValidator()
        self.name = "IAmiga"
        self.role = "Assistente Virtual do Programa Educa Grana"
    
    def apply_persona(self, response: str, question: str = "") -> Tuple[str, bool, List[PersonaViolation]]:
        """Aplica a persona a resposta e retorna versao corrigida."""
        
        is_valid, violations = self.validator.validate_response(response, question)
        corrected_response = self.validator.auto_fix_response(response, violations)
        final_is_valid, remaining_violations = self.validator.validate_response(corrected_response, question)
        
        return corrected_response, final_is_valid, remaining_violations
    
    def format_error_response(self, error_message: str = "") -> str:
        """Gera resposta de erro seguindo a persona."""
        return f"""Ops! Tive um probleminha tecnico, mas estou aqui para ajudar!

{error_message if error_message else "Tente reformular sua pergunta ou pergunte sobre:"}

Posso ajudar com:
- Programa Educa Grana
- Documentacao necessaria
- Avaliacao de carteira
- Educacao financeira

Como posso ajudar voce hoje?

IAmiga - Assistente Virtual do Educa Grana"""
    
    def format_off_topic_response(self) -> str:
        """Resposta padrao para topicos fora do escopo."""
        return """Entendo sua curiosidade, mas eu sou especializada em assuntos do Programa Educa Grana!

Posso ajudar voce com:
- Informacoes sobre microcredito
- Processos e documentacao  
- Avaliacao de carteira
- Educacao financeira
- Servicos do Banco do Nordeste

Como posso ajudar voce com o Educa Grana hoje?

IAmiga - Assistente Virtual do Educa Grana"""

def validate_iamiga_response(response: str, question: str = "") -> Tuple[str, bool]:
    """Funcao simples para validar e corrigir resposta da IAmiga."""
    persona = IAmigaPersona()
    corrected_response, is_valid, violations = persona.apply_persona(response, question)
    
    if violations:
        logger.info(f"Persona applied with {len(violations)} corrections")
    
    return corrected_response, is_valid