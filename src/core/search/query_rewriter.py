# src/core/search/query_rewriter.py
from __future__ import annotations
from typing import Dict, List, Tuple
import json
import re
import unicodedata
from pathlib import Path

_WORD_RE = re.compile(r"\b[\wÀ-ÖØ-öø-ÿ\-+/.]+\b", re.UNICODE)


def strip_accents(s: str) -> str:
    """Remove acentos e diacríticos de uma string."""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def singularize_pt(token: str) -> str:
    """
    Aplica regras simples de singularização para português.
    Regras comuns: ções→ção, ões→ão, ães→ão, sufixo s simples.
    """
    t = token.lower()
    
    # regras mais frequentes (simples e determinísticas)
    # ções → ção (operações → operação; condições → condição)
    if t.endswith("ções"):
        return t[:-4] + "ção"
    
    # ões → ão (operações → operação para caso sem 'ç', limões → limão)
    if t.endswith("ões"):
        return t[:-3] + "ão"
    
    # ães → ão (pães→pão, capitães→capitão)
    if t.endswith("ães"):
        return t[:-3] + "ão"
    
    # ais → al (animais → animal)
    if t.endswith("ais") and len(t) > 4:
        return t[:-3] + "al"
    
    # éis → el (papéis → papel)
    if t.endswith("éis") and len(t) > 4:
        return t[:-3] + "el"
    
    # simples plural → singular (remove 's' final)
    # Verificar se não termina com 'ss' ou outras exceções
    if t.endswith("s") and len(t) > 3 and not t.endswith("ss"):
        return t[:-1]
    
    return t


def normalize_token(token: str) -> str:
    """
    Normaliza um token: singulariza PRIMEIRO, depois remove acentos.
    Exemplo: 'operações' → 'operação' → 'operacao'
    """
    singular = singularize_pt(token.lower())
    return strip_accents(singular)

class QueryRewriter:
    def __init__(self, glossario_path: str):
        self.glossario = self._load(glossario_path)
        self.aliases: Dict[str, List[str]] = self.glossario.get("aliases", {})
        self.stop_expansion_in = set(map(str.lower, self.glossario.get("stop_expansion_in", [])))

    @staticmethod
    def _load(path: str) -> Dict:
        p = Path(path)
        if not p.exists():
            return {"aliases": {}, "stop_expansion_in": []}
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _looks_sensitive(self, token: str) -> bool:
        # Números longos (operacao/CPF) e padrões de CPF: não expandir
        if re.fullmatch(r"\d{6,}", token):
            return True
        if re.fullmatch(r"\d{3}\.?\d{3}\.?\d{3}\-?\d{2}", token):
            return True
        return False

    def _should_expand(self, token: str) -> bool:
        if token.lower() in self.stop_expansion_in:
            return False
        if self._looks_sensitive(token):
            return False
        return True

    def rewrite(self, query: str) -> Tuple[str, List[str]]:
        """
        Reescreve a query normalizando tokens (remove acentos + singulariza)
        e expandindo com sinônimos do glossário.
        """
        # 1. Extrair tokens raw da query
        raw_terms = _WORD_RE.findall(query.lower())
        
        # 2. Normalizar todos os tokens (remove acentos + singulariza)
        terms = [normalize_token(t) for t in raw_terms]
        
        # 3. Expandir com sinônimos do glossário (baseado em termos normalizados)
        expansions: List[str] = []
        for t in terms:
            if self._should_expand(t):
                # Buscar aliases normalizados
                for alias_key, alias_values in self.aliases.items():
                    normalized_key = normalize_token(alias_key)
                    if t == normalized_key:
                        # Normalizar sinônimos e adicionar apenas os que não estão presentes
                        syns = [normalize_token(s) for s in alias_values 
                               if normalize_token(s) not in terms]
                        expansions.extend(syns)
        
        # 4. Combinar termos originais + expansões (sem duplicatas)
        expanded = terms + [e for e in expansions if e not in terms]
        
        return " ".join(expanded), expansions
