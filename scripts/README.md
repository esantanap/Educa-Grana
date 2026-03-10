# 📊 Scripts de Análise e Feedback Loop

Scripts para análise de telemetria e aprendizado contínuo do sistema IAmiga.

## 📁 Estrutura

```
scripts/
├── analyze_telemetry.py          # Análise de telemetria + dashboard HTML
├── suggest_glossary_updates.py   # Sugestões de melhorias no glossário
└── run_weekly_analysis.py         # Script integrado (executar semanalmente)
```

## 🚀 Como Usar

### 1. Análise de Telemetria (Dashboard HTML)

```bash
python scripts/analyze_telemetry.py
```

**Gera:**
- `data/telemetry_report.html` - Dashboard visual com métricas

**Métricas incluídas:**
- Taxa de expansão de queries
- Satisfação dos usuários (👍/👎)
- Top queries mais frequentes
- Documentos com mais votos negativos
- Termos candidatos ao glossário

---

### 2. Sugestões de Glossário

```bash
python scripts/suggest_glossary_updates.py
```

**Gera:**
- `data/glossary_suggestions.md` - Relatório com sugestões

**Sugestões incluídas:**
- Novos termos para adicionar ao glossário
- Relações entre termos (co-ocorrências)
- Ajustes de `doc_boosts` baseado em votos

---

### 3. Análise Completa (RECOMENDADO)

```bash
python scripts/run_weekly_analysis.py
```

**Executa:**
- Análise de telemetria
- Sugestões de glossário
- Resumo executivo

**Abre automaticamente:** Dashboard HTML no navegador

---

## 📅 Execução Agendada

### Windows (Task Scheduler)

1. Abrir "Agendador de Tarefas"
2. Criar Tarefa Básica
3. Configurar:
   - Nome: "IAmiga Weekly Analysis"
   - Gatilho: Semanal (toda segunda-feira, 9h)
   - Ação: Iniciar programa
     - Programa: `C:\Users\...\venv\Scripts\python.exe`
     - Argumentos: `scripts\run_weekly_analysis.py`
     - Iniciar em: `C:\Users\...\miamiga`

### Linux/Mac (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha (toda segunda-feira, 9h)
0 9 * * 1 cd /path/to/miamiga && ./venv/bin/python scripts/run_weekly_analysis.py
```

---

## 📊 Exemplo de Workflow

### Ciclo de Melhoria Contínua

```
1. COLETA (1 semana)
   └─> Usuários usam o sistema
   └─> Telemetria registra queries + votos

2. ANÁLISE (segunda-feira)
   └─> Script semanal gera relatórios
   └─> Identifica padrões e problemas

3. AJUSTES (review time)
   └─> Adicionar novos aliases ao glossário
   └─> Ajustar doc_boosts
   └─> Atualizar src/core/domain/glossario.json

4. VALIDAÇÃO (1 semana)
   └─> Monitorar impacto das mudanças
   └─> Comparar métricas antes/depois

5. REPETIR
```

---

## 🎯 Métricas de Sucesso

| Métrica | Meta | Como Melhorar |
|---------|------|---------------|
| Taxa de Expansão | > 60% | Adicionar mais aliases |
| Satisfação | > 75% | Revisar queries com 👎 |
| Avg Resultados | 3-7 docs | Ajustar re-ranking |

---

## 🔧 Troubleshooting

**"Nenhum evento encontrado"**
- Verifique se `data/telemetry.log` existe
- Execute algumas queries no Streamlit primeiro

**"Poucos dados de votos"**
- Use o sistema por pelo menos 1 semana
- Incentive usuários a votar (👍👎)

**"Relatório HTML não abre"**
- Verifique permissões em `data/`
- Abra manualmente: `data/telemetry_report.html`

---

## 📝 Logs

Todos os scripts geram logs detalhados no terminal:

```
✅ Carregados X eventos (Y queries, Z votos)
🔄 Analisando expansão de queries...
👍 Analisando votos...
📄 Gerando relatório...
```

---

**Criado em:** 2026-01-13
**Última atualização:** 2026-01-13
