#!/usr/bin/env python3
# scripts/suggest_glossary_updates.py
"""
Analisa telemetria e votos para sugerir atualizações no glossário.
Identifica termos que precisam de aliases e ajusta pesos de doc_boosts.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

# Adicionar src/ ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from core.search.query_rewriter import normalize_token


class GlossarySuggester:
    def __init__(self, 
                 telemetry_path: str = "data/telemetry.log",
                 glossario_path: str = "src/core/domain/glossario.json"):
        self.telemetry_path = Path(telemetry_path)
        self.glossario_path = Path(glossario_path)
        self.glossario = self._load_glossario()
        self.queries = []
        self.votes = []
        
    def _load_glossario(self) -> Dict:
        """Carrega o glossário atual."""
        if not self.glossario_path.exists():
            return {"aliases": {}, "stop_expansion_in": [], "doc_boosts": {}}
        
        with open(self.glossario_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_telemetry(self):
        """Carrega dados de telemetria."""
        if not self.telemetry_path.exists():
            print(f"⚠️  Arquivo {self.telemetry_path} não encontrado")
            return
        
        with open(self.telemetry_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if event.get('event') == 'query_rewrite_rerank':
                        self.queries.append(event)
                    elif event.get('event') == 'vote':
                        self.votes.append(event)
                except json.JSONDecodeError:
                    continue
        
        print(f"✅ Carregados {len(self.queries)} queries, {len(self.votes)} votos")
    
    def suggest_new_aliases(self, min_frequency: int = 3) -> List[Tuple[str, int, List[str]]]:
        """
        Sugere novos termos para adicionar ao glossário.
        Retorna: [(termo, frequência, contexto_palavras)]
        """
        # Termos que aparecem em queries sem expansão
        no_expansion_terms = defaultdict(list)
        
        for q in self.queries:
            if not q.get('added_terms'):  # Query não expandiu
                original = q.get('original_query', '').lower()
                tokens = original.split()
                
                for i, token in enumerate(tokens):
                    normalized = normalize_token(token)
                    
                    # Filtrar stopwords e termos muito curtos
                    if len(normalized) <= 3:
                        continue
                    if normalized in ['qual', 'como', 'quai', 'onde', 'quando', 'porque', 'para', 'pela', 'pelo']:
                        continue
                    
                    # Verificar se já está no glossário
                    if normalized in self.glossario.get('aliases', {}):
                        continue
                    
                    # Capturar contexto (palavras ao redor)
                    context = []
                    if i > 0:
                        context.append(normalize_token(tokens[i-1]))
                    if i < len(tokens) - 1:
                        context.append(normalize_token(tokens[i+1]))
                    
                    no_expansion_terms[normalized].extend(context)
        
        # Contar frequência e agregar contexto
        suggestions = []
        for term, contexts in no_expansion_terms.items():
            frequency = len(contexts) // 2  # Aproximação (cada query contribui ~2 contextos)
            if frequency >= min_frequency:
                # Palavras mais comuns no contexto deste termo
                common_context = [w for w, _ in Counter(contexts).most_common(5) if w != term]
                suggestions.append((term, frequency, common_context))
        
        # Ordenar por frequência
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions
    
    def suggest_alias_expansions(self) -> List[Tuple[str, str, int]]:
        """
        Identifica pares de termos que aparecem juntos e sugere criar aliases.
        Retorna: [(termo1, termo2, co-ocorrência)]
        """
        # Extrair pares de termos que aparecem juntas
        term_pairs = Counter()
        
        for q in self.queries:
            original = q.get('original_query', '').lower()
            tokens = [normalize_token(t) for t in original.split()]
            
            # Filtrar stopwords
            tokens = [t for t in tokens if len(t) > 3 and t not in ['qual', 'como', 'quai', 'onde', 'quando']]
            
            # Contar pares
            for i in range(len(tokens)):
                for j in range(i+1, len(tokens)):
                    pair = tuple(sorted([tokens[i], tokens[j]]))
                    term_pairs[pair] += 1
        
        # Filtrar pares relevantes (min 3 ocorrências)
        suggestions = []
        for (term1, term2), count in term_pairs.items():
            if count >= 3:
                # Verificar se já existe alias
                aliases1 = self.glossario.get('aliases', {}).get(term1, [])
                aliases2 = self.glossario.get('aliases', {}).get(term2, [])
                
                if term2 not in aliases1 and term1 not in aliases2:
                    suggestions.append((term1, term2, count))
        
        suggestions.sort(key=lambda x: x[2], reverse=True)
        return suggestions[:15]  # Top 15
    
    def suggest_doc_boost_adjustments(self) -> Dict[str, Dict]:
        """
        Analisa votos para sugerir ajustes nos pesos de doc_boosts.
        Retorna: {doc_kind: {'current_boost': X, 'suggested_boost': Y, 'reason': '...'}}
        """
        if not self.votes:
            return {}
        
        # Contar votos por tipo de documento
        doc_votes = defaultdict(lambda: {'up': 0, 'down': 0})
        
        for vote in self.votes:
            vote_type = vote.get('vote')
            doc_ids = vote.get('doc_ids', [])
            
            # Tentar extrair o "kind" do doc_id (assumindo padrão como "1102-procedimento-...")
            for doc_id in doc_ids:
                # Heurística: se contém palavras-chave
                doc_lower = doc_id.lower()
                if 'normativo' in doc_lower or 'norma' in doc_lower:
                    kind = 'normativo'
                elif 'procedimento' in doc_lower or 'proc' in doc_lower:
                    kind = 'procedimento'
                elif 'apresentacao' in doc_lower or 'apresent' in doc_lower:
                    kind = 'apresentacao'
                elif 'fluxo' in doc_lower:
                    kind = 'fluxo_operacional'
                else:
                    kind = 'oneoff_nota'
                
                doc_votes[kind][vote_type] += 1
        
        # Calcular ajustes
        current_boosts = self.glossario.get('doc_boosts', {})
        suggestions = {}
        
        for kind, votes in doc_votes.items():
            total = votes['up'] + votes['down']
            if total < 3:  # Poucos dados
                continue
            
            satisfaction = votes['up'] / total if total > 0 else 0.5
            current_boost = current_boosts.get(kind, 1.0)
            
            # Sugerir ajuste
            if satisfaction > 0.8:  # Muito bom
                suggested = min(current_boost + 0.1, 1.5)
                reason = f"Alta satisfação ({satisfaction*100:.0f}%)"
            elif satisfaction < 0.4:  # Ruim
                suggested = max(current_boost - 0.15, 0.7)
                reason = f"Baixa satisfação ({satisfaction*100:.0f}%)"
            else:  # Neutro
                suggested = current_boost
                reason = f"Satisfação moderada ({satisfaction*100:.0f}%)"
            
            if abs(suggested - current_boost) > 0.05:  # Mudança significativa
                suggestions[kind] = {
                    'current_boost': current_boost,
                    'suggested_boost': round(suggested, 2),
                    'satisfaction': f"{satisfaction*100:.0f}%",
                    'votes': f"👍{votes['up']} 👎{votes['down']}",
                    'reason': reason
                }
        
        return suggestions
    
    def generate_suggestions_report(self, output_path: str = "data/glossary_suggestions.md"):
        """Gera relatório em Markdown com sugestões."""
        new_aliases = self.suggest_new_aliases()
        alias_expansions = self.suggest_alias_expansions()
        boost_adjustments = self.suggest_doc_boost_adjustments()
        
        report = f"""# 📝 Sugestões de Atualização do Glossário

**Data:** {Path(output_path).stem}
**Baseado em:** {len(self.queries)} queries processadas, {len(self.votes)} votos

---

## 1️⃣ Novos Termos Candidatos ao Glossário

Termos que aparecem frequentemente em queries **sem expansão** (podem precisar de aliases):

| Termo | Freq. | Contexto Comum | Sugestão de Aliases |
|-------|-------|----------------|---------------------|
"""
        
        for term, freq, context in new_aliases[:20]:
            context_str = ', '.join(context[:3]) if context else '-'
            report += f"| **{term}** | {freq}x | {context_str} | _sugerir manualmente_ |\n"
        
        report += f"""

## 2️⃣ Sugestões de Relação entre Termos

Pares de termos que aparecem frequentemente juntos (podem ser aliases um do outro):

| Termo 1 | Termo 2 | Co-ocorrências | Ação Sugerida |
|---------|---------|----------------|---------------|
"""
        
        for term1, term2, count in alias_expansions:
            report += f"| {term1} | {term2} | {count}x | Adicionar `{term2}` aos aliases de `{term1}`? |\n"
        
        report += """

## 3️⃣ Ajustes de Boost por Tipo de Documento

Baseado em votos (👍/👎), sugestões de ajuste nos pesos `doc_boosts`:

| Tipo Doc | Boost Atual | Boost Sugerido | Satisfação | Votos | Motivo |
|----------|-------------|----------------|------------|-------|--------|
"""
        
        if boost_adjustments:
            for kind, data in boost_adjustments.items():
                report += f"| {kind} | {data['current_boost']} | **{data['suggested_boost']}** | {data['satisfaction']} | {data['votes']} | {data['reason']} |\n"
        else:
            report += "| - | - | - | - | - | _Poucos dados de votos_ |\n"
        
        report += """

---

## 📋 Como Aplicar as Sugestões

### Para adicionar novo alias:
```json
{
  "aliases": {
    "novo_termo": ["sinonimo1", "sinonimo2", "ccb", "contrato"]
  }
}
```

### Para ajustar doc_boosts:
```json
{
  "doc_boosts": {
    "normativo": 1.25,
    "procedimento": 1.15
  }
}
```

### Após aplicar:
1. Edite `src/core/domain/glossario.json`
2. Reinicie o agente
3. Teste queries afetadas
4. Monitore telemetria por mais 1 semana

---
**Gerado automaticamente por:** `scripts/suggest_glossary_updates.py`
"""
        
        output_file = Path(output_path)
        output_file.write_text(report, encoding='utf-8')
        print(f"\n✅ Relatório de sugestões gerado: {output_file.absolute()}")
        return str(output_file.absolute())


def main():
    print("=" * 80)
    print("🔍 SUGESTÕES DE ATUALIZAÇÃO DO GLOSSÁRIO - IAmiga")
    print("=" * 80)
    
    suggester = GlossarySuggester()
    suggester.load_telemetry()
    
    if not suggester.queries:
        print("\n⚠️  Nenhuma query encontrada. Execute algumas queries primeiro!")
        return
    
    print("\n📝 Identificando novos termos candidatos...")
    new_aliases = suggester.suggest_new_aliases()
    print(f"   Encontrados: {len(new_aliases)} termos")
    if new_aliases:
        print(f"   Top 3: {[t[0] for t in new_aliases[:3]]}")
    
    print("\n🔗 Identificando relações entre termos...")
    expansions = suggester.suggest_alias_expansions()
    print(f"   Encontradas: {len(expansions)} relações")
    
    print("\n⚖️  Analisando ajustes de doc_boosts...")
    boosts = suggester.suggest_doc_boost_adjustments()
    if boosts:
        print(f"   Sugeridos ajustes para: {list(boosts.keys())}")
    else:
        print("   Poucos dados de votos para sugerir ajustes")
    
    print("\n📄 Gerando relatório de sugestões...")
    report_path = suggester.generate_suggestions_report()
    
    print("\n" + "=" * 80)
    print(f"✅ Análise concluída!")
    print(f"📂 Veja sugestões em: {report_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
