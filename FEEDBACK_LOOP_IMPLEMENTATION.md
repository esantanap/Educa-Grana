# 🎯 Sistema de Feedback Loop e Análise - IAmiga - IMPLEMENTADO

## ✅ O que foi implementado

### 1. **Análise de Telemetria** (`scripts/analyze_telemetry.py`)

**Funcionalidades:**
- ✅ Dashboard HTML visual com métricas em tempo real
- ✅ Análise de taxa de expansão de queries
- ✅ Análise de votos (👍/👎) e satisfação
- ✅ Identificação de queries problemáticas
- ✅ Identificação de documentos com baixa relevância
- ✅ Top termos adicionados e queries mais frequentes

**Métricas rastreadas:**
- Total de eventos processados
- Taxa de expansão (% queries expandidas)
- Taxa de satisfação (% thumbs up)
- Top 10 termos adicionados
- Top 15 queries mais frequentes
- Queries com mais votos negativos
- Documentos com mais votos negativos

---

### 2. **Sugestões de Glossário** (`scripts/suggest_glossary_updates.py`)

**Funcionalidades:**
- ✅ Identifica termos candidatos ao glossário (aparecem sem expandir)
- ✅ Sugere relações entre termos (co-ocorrências)
- ✅ Ajusta `doc_boosts` baseado em votos
- ✅ Gera relatório Markdown com ações recomendadas

**Análises incluídas:**
1. **Novos termos:** Palavras frequentes em queries não expandidas
2. **Relações:** Pares de termos que aparecem juntos (ex: "prazo + operacao")
3. **Ajustes de boost:** Aumentar/diminuir peso por tipo de documento

**Exemplo de saída:**
```markdown
## Ajustes de Boost por Tipo de Documento

| Tipo Doc | Boost Atual | Boost Sugerido | Satisfação | Votos | Motivo |
|----------|-------------|----------------|------------|-------|--------|
| procedimento | 1.25 | **1.35** | 100% | 👍3 👎0 | Alta satisfação |
| apresentacao | 1.1 | **0.95** | 0% | 👍0 👎2 | Baixa satisfação |
```

---

### 3. **Script Integrado Semanal** (`scripts/run_weekly_analysis.py`)

**Funcionalidades:**
- ✅ Executa análise completa com um comando
- ✅ Combina telemetria + sugestões de glossário
- ✅ Gera resumo executivo no terminal
- ✅ Opção de abrir dashboard HTML automaticamente

**Uso:**
```bash
python scripts/run_weekly_analysis.py
```

**Saída:**
```
📈 MÉTRICAS PRINCIPAIS:
   • Total de eventos: 10
   • Queries processadas: 5
   • Taxa de expansão: 40.0%
   • Taxa de satisfação: 60.0%
   • Votos: 👍 3 | 👎 2

📂 RELATÓRIOS GERADOS:
   1. HTML Dashboard: data/telemetry_report.html
   2. Sugestões MD: data/glossary_suggestions.md
```

---

## 🔄 Ciclo de Melhoria Contínua

```
┌─────────────────────────────────────────────────────────────┐
│ 1. COLETA (contínua)                                        │
│    └─> Usuários usam sistema                                │
│    └─> Telemetria registra queries + votos                  │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ANÁLISE (semanal)                                        │
│    └─> run_weekly_analysis.py                               │
│    └─> Gera dashboard HTML + sugestões MD                   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. REVISÃO (manual)                                         │
│    └─> Analista revisa relatórios                           │
│    └─> Identifica padrões e oportunidades                   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. AJUSTES (aplicar mudanças)                               │
│    └─> Editar src/core/domain/glossario.json                │
│    └─> Adicionar novos aliases                              │
│    └─> Ajustar doc_boosts                                   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. VALIDAÇÃO (1 semana)                                     │
│    └─> Monitorar impacto das mudanças                       │
│    └─> Comparar métricas antes/depois                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       └──────> REPETIR ──────┐
                                              │
                                              ▼
                                        (volta ao 1)
```

---

## 📊 Exemplo de Insights Gerados

### Cenário Real (do teste):

**Dados:**
- 8 queries processadas
- 75% taxa de expansão
- 1 voto negativo

**Insights automáticos:**
1. ✅ "operacao" e "prazo" aparecem juntos 5x → sugerir alias
2. ✅ "crediamigo" e "prazo" aparecem juntos 4x → sugerir alias
3. ⚠️ Satisfação 0% → investigar queries com 👎

**Ações recomendadas:**
```json
{
  "aliases": {
    "operacao": ["emprestimo", "contrato", "ccb", "prazo"],
    "crediamigo": ["programa", "microcredito", "prazo"]
  }
}
```

---

## 🚀 Como Usar

### Execução Manual
```bash
# Análise completa (recomendado)
python scripts/run_weekly_analysis.py

# Apenas telemetria
python scripts/analyze_telemetry.py

# Apenas sugestões
python scripts/suggest_glossary_updates.py
```

### Execução Agendada (Windows)
1. Agendador de Tarefas → Criar Tarefa Básica
2. Gatilho: Semanal (segunda-feira, 9h)
3. Ação: `python.exe scripts\run_weekly_analysis.py`

### Execução Agendada (Linux/Mac)
```bash
# Crontab (toda segunda-feira, 9h)
0 9 * * 1 cd /path/to/miamiga && python scripts/run_weekly_analysis.py
```

---

## 📈 Metas de Sucesso

| Métrica | Meta | Ação se abaixo da meta |
|---------|------|------------------------|
| Taxa de Expansão | > 60% | Adicionar mais aliases ao glossário |
| Satisfação | > 75% | Revisar queries com 👎, melhorar docs |
| Avg Resultados | 3-7 | Ajustar re-ranking, calibrar boosts |

---

## 🎁 Benefícios

1. ✅ **Aprendizado Contínuo:** Sistema melhora automaticamente com o uso
2. ✅ **Data-Driven:** Decisões baseadas em dados reais de telemetria
3. ✅ **Low Effort:** Scripts automatizados reduzem trabalho manual
4. ✅ **Métricas Visíveis:** Dashboard HTML facilita comunicação com stakeholders
5. ✅ **Feedback Loop:** Votos dos usuários → Melhorias → Mais satisfação

---

## 📂 Arquivos Criados

```
scripts/
├── analyze_telemetry.py          # 250 linhas - Análise + HTML
├── suggest_glossary_updates.py   # 220 linhas - Sugestões + MD
├── run_weekly_analysis.py         # 80 linhas - Script integrado
└── README.md                      # Documentação

data/
├── telemetry.log                  # Eventos de produção
├── telemetry_report.html          # Dashboard visual
└── glossary_suggestions.md        # Sugestões de melhorias
```

---

**Status:** ✅ IMPLEMENTADO E TESTADO
**Data:** 2026-01-13
**Próximo passo:** Usar em produção por 1 semana e revisar relatórios!
