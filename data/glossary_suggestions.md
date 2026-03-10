# 📝 Sugestões de Atualização do Glossário

**Data:** glossary_suggestions
**Baseado em:** 94 queries processadas, 10 votos

---

## 1️⃣ Novos Termos Candidatos ao Glossário

Termos que aparecem frequentemente em queries **sem expansão** (podem precisar de aliases):

| Termo | Freq. | Contexto Comum | Sugestão de Aliases |
|-------|-------|----------------|---------------------|
| **Educa Grana** | 20x | do, ?, e | _sugerir manualmente_ |
| **credito?** | 8x | de, solicitar | _sugerir manualmente_ |
| **documento** | 6x | qual, necessario, os | _sugerir manualmente_ |
| **contratar** | 5x | ?, posso, para | _sugerir manualmente_ |
| **posso** | 4x | contratar, produto, como | _sugerir manualmente_ |
| **listar** | 4x | ou, as | _sugerir manualmente_ |
| **preciso** | 3x | documento, ?, para | _sugerir manualmente_ |
| **individual** | 3x | ?, credito, Educa Grana | _sugerir manualmente_ |
| **disponivei** | 3x | credito, no, estao | _sugerir manualmente_ |
| **comun** | 3x | mai, do | _sugerir manualmente_ |
| **capital** | 3x | de, credito:, e | _sugerir manualmente_ |
| **disponiveis?** | 3x | credito | _sugerir manualmente_ |


## 2️⃣ Sugestões de Relação entre Termos

Pares de termos que aparecem frequentemente juntos (podem ser aliases um do outro):

| Termo 1 | Termo 2 | Co-ocorrências | Ação Sugerida |
|---------|---------|----------------|---------------|
| credito | linha | 21x | Adicionar `linha` aos aliases de `credito`? |
| credito? | linha | 20x | Adicionar `linha` aos aliases de `credito?`? |
| Educa Grana | credito | 12x | Adicionar `credito` aos aliases de `Educa Grana`? |
| Educa Grana | linha | 9x | Adicionar `linha` aos aliases de `Educa Grana`? |
| disponiveis? | linha | 7x | Adicionar `linha` aos aliases de `disponiveis?`? |
| credito | disponiveis? | 7x | Adicionar `disponiveis?` aos aliases de `credito`? |
| operacao | prazo | 5x | Adicionar `prazo` aos aliases de `operacao`? |
| emprestimo | tipo | 5x | Adicionar `tipo` aos aliases de `emprestimo`? |
| Educa Grana | emprestimo | 5x | Adicionar `emprestimo` aos aliases de `Educa Grana`? |
| credito? | solicitar | 5x | Adicionar `solicitar` aos aliases de `credito?`? |
| Educa Grana | prazo | 4x | Adicionar `prazo` aos aliases de `Educa Grana`? |
| Educa Grana | delas? | 4x | Adicionar `delas?` aos aliases de `Educa Grana`? |
| documento | necessario | 4x | Adicionar `necessario` aos aliases de `documento`? |
| documento | para | 4x | Adicionar `para` aos aliases de `documento`? |
| contratar | posso | 4x | Adicionar `posso` aos aliases de `contratar`? |


## 3️⃣ Ajustes de Boost por Tipo de Documento

Baseado em votos (👍/👎), sugestões de ajuste nos pesos `doc_boosts`:

| Tipo Doc | Boost Atual | Boost Sugerido | Satisfação | Votos | Motivo |
|----------|-------------|----------------|------------|-------|--------|
| - | - | - | - | - | _Poucos dados de votos_ |


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
