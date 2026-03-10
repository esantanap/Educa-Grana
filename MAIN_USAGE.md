# 🚀 IAmiga - Sistema Modular

Sistema modularizado com orquestrador `main.py` que permite executar diferentes componentes separadamente ou todos de uma vez.

## 🎯 Início Rápido - Iniciar Tudo

```bash
python main.py start
```

Este comando irá:
- ✅ Iniciar 3 servidores simultaneamente
- ✅ Abrir 3 abas no navegador automaticamente
- ✅ Exibir URLs de acesso

**Servidores iniciados:**
- 🌐 **Interface Web:** http://10.85.72.29:8501
- 📋 **Logs:** http://10.85.72.29:8502
- 📊 **Métricas:** http://10.85.72.29:8503

**Para parar todos:** Pressione `Ctrl+C`

---

## 📋 Comandos Individuais

### 1. Interface Web Principal
```bash
python main.py web
```
**Opções:**
- `--host` - Host (padrão: 0.0.0.0)
- `--port` - Porta (padrão: 8501)

**Acesso:** http://10.85.72.29:8501

---

### 2. Servidor de Logs (Independente)
```bash
python main.py logs
```
**Opções:**
- `--port` - Porta (padrão: 8502)

**Acesso:** http://10.85.72.29:8502

**Funcionalidades:**
- 📋 Visualização de logs em tempo real
- 🔍 Filtros por nível (INFO, WARNING, ERROR)
- 🔍 Busca por texto
- 🔄 Auto-atualização configurável
- 📊 Estatísticas de logs

---

### 3. Servidor de Métricas (Independente)
```bash
python main.py metrics
```
**Opções:**
- `--port` - Porta (padrão: 8503)

**Exemplo:**
```bash
python main.py metrics --port 8503
```
**Acesso:** http://10.85.72.29:8503

**Funcionalidades:**
- 📊 Dashboard HTML completo (telemetry_report.html)
- 🔄 Botão para atualizar relatório
- 📈 Gráficos e estatísticas de uso
- 👍👎 Análise de feedback
- ⚠️ Violações de guardrails

---

### 4. Processar Documentos
```bash
python main.py process
```
Executa o script `create_vectordb.py` para processar PDFs e criar a base de conhecimento.

---

### 5. Análise de Telemetria
```bash
python main.py analyze
```
Gera o relatório HTML de telemetria executando `scripts/analyze_telemetry.py`.

---

## 🎯 Benefícios da Arquitetura Modular

### ✅ Desacoplamento
- Cada componente roda independentemente
- Logs e métricas não afetam a aplicação principal
- Facilita manutenção e debugging

### ✅ Escalabilidade
- Possível rodar em servidores diferentes
- Balanceamento de carga por componente
- Recursos dedicados para cada serviço

### ✅ Desenvolvimento
- Teste de componentes isoladamente
- Deploy independente de cada módulo
- Facilita refatoração

---

## 🔧 Uso em Produção

### Executar todos os componentes:

**Terminal 1 - Interface Principal:**
```bash
python main.py web --port 8501
```

**Terminal 2 - Logs:**
```bash
python main.py logs --port 8502
```

**Terminal 3 - Métricas:**
```bash
python main.py metrics --port 8503
```

### Acessos:
- **App Principal:** http://10.85.72.29:8501
- **Logs:** http://10.85.72.29:8502
- **Métricas:** http://10.85.72.29:8503

---

## 📝 Ajuda

```bash
python main.py --help
```

Ver ajuda de um comando específico:
```bash
python main.py web --help
python main.py logs --help
python main.py metrics --help
```

---

## 🔄 Migração do Sistema Antigo

**Antes:**
```bash
streamlit run src\core\frontend\app.py
```

**Agora:**
```bash
python main.py web
```

**Vantagens:**
- Mesmo resultado
- Mais controle sobre parâmetros
- Facilita automação
- Comandos padronizados
