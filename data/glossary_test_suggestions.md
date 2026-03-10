# 📝 Sugestões de Atualização do Glossário

**Data:** glossary_test_suggestions
**Baseado em:** 5 queries processadas, 5 votos

---

## 1️⃣ Novos Termos Candidatos ao Glossário

Termos que aparecem frequentemente em queries **sem expansão** (podem precisar de aliases):

| Termo | Freq. | Contexto Comum | Sugestão de Aliases |
|-------|-------|----------------|---------------------|


## 2️⃣ Sugestões de Relação entre Termos

Pares de termos que aparecem frequentemente juntos (podem ser aliases um do outro):

| Termo 1 | Termo 2 | Co-ocorrências | Ação Sugerida |
|---------|---------|----------------|---------------|


## 3️⃣ Ajustes de Boost por Tipo de Documento

Baseado em votos (👍/👎), sugestões de ajuste nos pesos `doc_boosts`:

| Tipo Doc | Boost Atual | Boost Sugerido | Satisfação | Votos | Motivo |
|----------|-------------|----------------|------------|-------|--------|
| procedimento | 1.25 | **1.35** | 100% | 👍3 👎0 | Alta satisfação (100%) |


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
