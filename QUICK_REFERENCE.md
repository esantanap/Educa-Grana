# 🚀 Guia de Referência Rápida - IAmiga

## 📋 Comandos Essenciais

### Iniciar o Sistema
```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Iniciar Streamlit
streamlit run src\core\frontend\app.py
```

### Recriar Base de Conhecimento
```bash
# Reprocessar todos os PDFs
python src/create_vectordb.py
```

### Gerenciar Glossário
```bash
# Editor interativo (recomendado)
python scripts/add_to_glossary.py

# Ver glossário atual
Get-Content src/core/domain/glossario.json
```

### Análise e Telemetria
```bash
# Análise completa (semanal)
python scripts/run_weekly_analysis.py

# Apenas dashboard HTML
python scripts/analyze_telemetry.py

# Apenas sugestões de glossário
python scripts/suggest_glossary_updates.py
```

### Testes
```bash
# Testar normalização morfológica
python test_normalization.py

# Testar query rewrite completo
python test_query_rewrite.py

# Testar feedback loop
python test_feedback_loop.py
```

---

## 📂 Estrutura de Arquivos Importantes

```
miamiga/
├── src/
│   ├── agent.py                    # Agente RAG principal
│   ├── create_vectordb.py          # Processamento de PDFs
│   └── core/
│       ├── domain/
│       │   └── glossario.json      # ⭐ Glossário de domínio
│       ├── search/
│       │   ├── query_rewriter.py   # Query rewrite + normalização
│       │   └── reranker.py         # Re-ranking heurístico
│       └── frontend/
│           └── app.py              # Interface Streamlit
│
├── scripts/
│   ├── analyze_telemetry.py        # Análise de telemetria
│   ├── suggest_glossary_updates.py # Sugestões de glossário
│   ├── run_weekly_analysis.py      # ⭐ Script semanal completo
│   └── add_to_glossary.py          # ⭐ Editor interativo
│
├── data/
│   ├── knowledge_base.json         # Base vetorial (1035 docs)
│   ├── telemetry.log               # ⭐ Log de telemetria
│   ├── telemetry_report.html       # Dashboard visual
│   └── glossary_suggestions.md     # Sugestões automáticas
│
├── docs/                           # PDFs do Crediamigo (89 arquivos)
├── .env                            # Configurações (copiar de .env.example)
└── README.md                       # ⭐ Documentação principal
```

---

## 🔑 Arquivo .env (Configuração)

```bash
# API LLM
OPENAI_API_KEY=sua-chave-aqui
OPENAI_BASE_URL=https://api.bnb.internal/v1
OPENAI_MODEL=bnb-gpt-5-mini

# SSL/TLS
REQUESTS_CA_BUNDLE=C:\Users\...\certs\ca-bnb.pem
SSL_CERT_FILE=C:\Users\...\certs\ca-bnb.pem
ALLOW_INSECURE_SSL=false

# Logging
LOG_LEVEL=INFO
```

---

## 📖 Estrutura do Glossário

```json
{
  "aliases": {
    "operação": ["empréstimo", "contrato", "ccb"],
    "prazo": ["vencimento", "período", "duração"]
  },
  "stop_expansion_in": ["CNPJ", "CPF", "matrícula"],
  "doc_boosts": {
    "normativo": 1.3,
    "procedimento": 1.25,
    "apresentacao": 1.05
  }
}
```

---

## 🔄 Workflow de Melhoria Contínua

```
1. USAR (1 semana)
   └─> Usuários fazem perguntas
   └─> Sistema coleta telemetria (data/telemetry.log)

2. ANALISAR (segunda-feira)
   └─> python scripts/run_weekly_analysis.py
   └─> Abrir data/telemetry_report.html
   └─> Revisar data/glossary_suggestions.md

3. AJUSTAR
   └─> python scripts/add_to_glossary.py
   └─> Adicionar aliases sugeridos
   └─> Ajustar doc_boosts se necessário

4. VALIDAR (1 semana)
   └─> Monitorar métricas no próximo relatório
   └─> Comparar antes/depois

5. REPETIR
```

---

## 📊 Métricas de Sucesso

| Métrica | Meta | Como Melhorar |
|---------|------|---------------|
| Taxa de Expansão | > 60% | Adicionar mais aliases ao glossário |
| Satisfação (👍/👎) | > 75% | Revisar queries com votos negativos |
| Avg Resultados | 3-7 docs | Ajustar re-ranking e boosts |

---

## 🆘 Troubleshooting Rápido

### Sistema não inicia
```bash
# Verificar ambiente
.\venv\Scripts\activate
python --version  # Deve ser 3.13+

# Verificar .env
Test-Path .env  # Deve retornar True

# Verificar certificado SSL
Test-Path C:\Users\...\certs\ca-bnb.pem
```

### Glossário não está expandindo
```bash
# Reiniciar Streamlit (recarrega glossário)
Ctrl+C
streamlit run src\core\frontend\app.py

# Validar JSON
python -m json.tool src/core/domain/glossario.json
```

### Telemetria vazia
```bash
# Verificar arquivo
Test-Path data/telemetry.log
Get-Content data/telemetry.log | Measure-Object -Line

# Fazer algumas queries primeiro no Streamlit
# Depois executar análise
```

---

## 📚 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| [README.md](README.md) | Documentação principal do sistema |
| [COMO_ADICIONAR_AO_GLOSSARIO.md](COMO_ADICIONAR_AO_GLOSSARIO.md) | Guia completo do glossário |
| [FEEDBACK_LOOP_IMPLEMENTATION.md](FEEDBACK_LOOP_IMPLEMENTATION.md) | Sistema de análise e telemetria |
| [scripts/README.md](scripts/README.md) | Documentação dos scripts |
| [.env.example](.env.example) | Template de configuração |

---

## 🎯 Checklist Diário

- [ ] Streamlit rodando e acessível
- [ ] Usuários fazendo perguntas
- [ ] Telemetria sendo registrada (data/telemetry.log crescendo)
- [ ] Votos sendo coletados (👍👎)

## 🎯 Checklist Semanal (Segunda-feira)

- [ ] Executar: `python scripts/run_weekly_analysis.py`
- [ ] Abrir dashboard HTML gerado
- [ ] Revisar sugestões de glossário (MD)
- [ ] Aplicar melhorias relevantes
- [ ] Documentar mudanças no git commit

---

**Última atualização:** 2026-01-13
**Versão:** v2.1.0
