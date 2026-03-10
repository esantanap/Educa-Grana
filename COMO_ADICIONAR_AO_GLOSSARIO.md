# 📚 Guia: Como Adicionar Termos ao Glossário

## 🎯 Localização do Arquivo

**Arquivo:** `src/core/domain/glossario.json`

---

## 📝 Estrutura do Glossário

O glossário tem 3 seções principais:

### 1. **`aliases`** - Sinônimos e Expansões

Mapeia um termo principal → lista de sinônimos que serão adicionados à busca.

**Formato:**
```json
{
  "aliases": {
    "termo_principal": ["sinonimo1", "sinonimo2", "sinonimo3"]
  }
}
```

### 2. **`stop_expansion_in`** - Termos Protegidos

Lista de termos que NUNCA devem ser expandidos (dados sensíveis, IDs).

**Formato:**
```json
{
  "stop_expansion_in": ["CNPJ", "CPF", "número da operação"]
}
```

### 3. **`doc_boosts`** - Pesos por Tipo de Documento

Multiplica a relevância de documentos por tipo (maior = mais relevante).

**Formato:**
```json
{
  "doc_boosts": {
    "normativo": 1.3,
    "procedimento": 1.25
  }
}
```

---

## ✅ Exemplos Práticos

### Exemplo 1: Adicionar novo termo simples

**Cenário:** Usuários perguntam sobre "prazo" mas o sistema não expande

**Antes:**
```json
{
  "aliases": {
    "operação": ["empréstimo", "contrato", "ccb"]
  }
}
```

**Depois:**
```json
{
  "aliases": {
    "operação": ["empréstimo", "contrato", "ccb", "prazo", "vencimento"],
    "prazo": ["vencimento", "período", "tempo"]
  }
}
```

---

### Exemplo 2: Adicionar relação bidirecional

**Cenário:** "taxa" e "juros" devem se expandir mutuamente

**Adicionar:**
```json
{
  "aliases": {
    "taxa": ["juros", "percentual", "encargos"],
    "juros": ["taxa", "percentual", "encargos"]
  }
}
```

**Resultado:** 
- Query "qual a taxa?" → expande com "juros", "percentual", "encargos"
- Query "quanto de juros?" → expande com "taxa", "percentual", "encargos"

---

### Exemplo 3: Adicionar termo técnico com variações

**Cenário:** Diferentes formas de falar sobre "cliente"

**Adicionar:**
```json
{
  "aliases": {
    "cliente": ["tomador", "beneficiário", "empreendedor", "mutuário"]
  }
}
```

---

### Exemplo 4: Proteger termos sensíveis

**Cenário:** IDs e códigos não devem expandir

**Adicionar em `stop_expansion_in`:**
```json
{
  "stop_expansion_in": ["CNPJ", "CPF", "número da operação", "id do grupo", "matrícula", "código do agente"]
}
```

---

### Exemplo 5: Ajustar relevância por tipo de documento

**Cenário:** Documentos "normativo" estão aparecendo muito, mas usuários preferem "procedimento"

**Antes:**
```json
{
  "doc_boosts": {
    "normativo": 1.3,
    "procedimento": 1.25
  }
}
```

**Depois:**
```json
{
  "doc_boosts": {
    "normativo": 1.15,     // ⬇️ reduziu
    "procedimento": 1.35   // ⬆️ aumentou
  }
}
```

---

## 🤖 Aplicando Sugestões Automáticas

Quando você executa `python scripts/run_weekly_analysis.py`, ele gera:

**Arquivo:** `data/glossary_suggestions.md`

**Conteúdo exemplo:**
```markdown
## Sugestões de Relação entre Termos

| Termo 1 | Termo 2 | Co-ocorrências | Ação Sugerida |
|---------|---------|----------------|---------------|
| operacao | prazo | 5x | Adicionar `prazo` aos aliases de `operacao`? |
```

**Como aplicar:**

1. Abra `data/glossary_suggestions.md`
2. Revise as sugestões (nem todas são boas!)
3. Edite `src/core/domain/glossario.json`
4. Adicione os termos manualmente

**Exemplo:**
```json
{
  "aliases": {
    "operação": ["empréstimo", "contrato", "ccb", "prazo"]  // ✅ adicionado "prazo"
  }
}
```

---

## 🔄 Workflow Completo

```
1. IDENTIFICAR NECESSIDADE
   ├─> Revisar relatório: data/glossary_suggestions.md
   ├─> Verificar queries com muitos 👎
   └─> Identificar termos que não expandem

2. EDITAR GLOSSÁRIO
   ├─> Abrir: src/core/domain/glossario.json
   ├─> Adicionar aliases
   ├─> Ajustar doc_boosts (se necessário)
   └─> Salvar arquivo

3. VALIDAR SINTAXE JSON
   ├─> Verificar vírgulas
   ├─> Verificar aspas
   └─> Testar: python -m json.tool src/core/domain/glossario.json

4. REINICIAR SISTEMA
   ├─> Parar Streamlit (Ctrl+C)
   ├─> Reiniciar: streamlit run src/core/frontend/app.py
   └─> O glossário é recarregado automaticamente

5. TESTAR MUDANÇAS
   ├─> Fazer queries que devem expandir
   ├─> Verificar logs: [REWRITE] no terminal
   └─> Confirmar se os termos foram adicionados

6. MONITORAR (1 semana)
   ├─> Executar: python scripts/run_weekly_analysis.py
   ├─> Comparar métricas antes/depois
   └─> Ajustar se necessário
```

---

## ⚠️ Boas Práticas

### ✅ FAZER:

- **Normalizar termos** (singular, sem acento): `"operacao"` ✅
- **Adicionar variações comuns**: `"emprestimo"`, `"empréstimo"` ✅
- **Relações bidirecionais** quando faz sentido
- **Testar antes de commitar**
- **Documentar mudanças** (comentários no git commit)

### ❌ NÃO FAZER:

- **Adicionar stopwords** (`"o", "a", "de"`) ❌
- **Aliases muito genéricos** (`"documento": ["tudo"]`) ❌
- **Termos muito longos** (`"como fazer para solicitar um empréstimo"`) ❌
- **Duplicatas** (mesmo termo em múltiplas chaves) ❌
- **Esquecer vírgulas** (quebra o JSON) ❌

---

## 🧪 Validar JSON

Antes de salvar, sempre validar:

```bash
# Windows PowerShell
Get-Content src/core/domain/glossario.json | ConvertFrom-Json

# Ou Python
python -m json.tool src/core/domain/glossario.json
```

Se houver erro, você verá algo como:
```
Expecting ',' delimiter: line 12 column 5 (char 234)
```

---

## 📊 Verificar Impacto

Depois de adicionar termos, execute:

```bash
# Teste rápido
python test_query_rewrite.py

# Análise completa (após 1 semana de uso)
python scripts/run_weekly_analysis.py
```

**Métricas esperadas:**
- ✅ Taxa de expansão aumenta
- ✅ Satisfação melhora (mais 👍)
- ✅ Queries problemáticas diminuem

---

## 📂 Exemplo Completo (Glossário Atualizado)

```json
{
  "aliases": {
    "operação": ["empréstimo", "contrato", "ccb", "financiamento", "prazo"],
    "empréstimo": ["operação", "contrato", "ccb"],
    "prazo": ["vencimento", "período", "tempo", "duração"],
    "taxa": ["juros", "percentual", "encargos"],
    "juros": ["taxa", "percentual", "encargos"],
    "cliente": ["tomador", "beneficiário", "empreendedor"],
    "desembolso": ["liberação", "crédito liberado"],
    "parcela": ["prestação", "mensalidade"],
    "renovação": ["novo ciclo", "recontratação"],
    "grupo": ["grupo solidário", "grupo Educa Grana"]
  },
  "stop_expansion_in": [
    "CNPJ", 
    "CPF", 
    "número da operação", 
    "id do grupo",
    "matrícula",
    "código do agente"
  ],
  "doc_boosts": {
    "normativo": 1.3,
    "procedimento": 1.25,
    "fluxo_operacional": 1.2,
    "apresentacao": 1.05,
    "oneoff_nota": 1.0
  }
}
```

---

## 🆘 Troubleshooting

**Problema:** "Adicionei um termo mas não está expandindo"

**Soluções:**
1. Verificar se o termo está normalizado (sem acento, singular)
2. Reiniciar o Streamlit (o glossário é carregado no início)
3. Verificar logs: procurar por `[REWRITE]` no terminal
4. Testar com: `python test_normalization.py`

---

**Problema:** "Sistema quebrou após editar glossário"

**Soluções:**
1. Validar JSON: `python -m json.tool src/core/domain/glossario.json`
2. Verificar vírgulas e aspas
3. Restaurar do git: `git checkout src/core/domain/glossario.json`
4. Replicar mudanças com mais cuidado

---

**Problema:** "Taxa de expansão diminuiu após adicionar termos"

**Explicação:** Normal! Pode ser que os novos termos sejam muito específicos.

**Ação:** Revisar se os termos fazem sentido. Taxa ideal: 50-70%.

---

**Última atualização:** 2026-01-13
