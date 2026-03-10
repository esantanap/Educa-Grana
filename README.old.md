# 🤖 MiAmiga - Assistente Virtual Crediamigo

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.x-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![TF--IDF](https://img.shields.io/badge/Search-TF--IDF-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**Sistema RAG (Retrieval-Augmented Generation) especializado em consultas sobre o Programa Crediamigo do Banco do Nordeste**

[Instalação](#-instalação-rápida) • [Configuração](#️-configuração) • [Uso](#-como-usar) • [Segurança](#-segurança)

</div>

---

## 📖 Sobre o Projeto

O **MiAmiga** é a assistente virtual especializada do Programa Crediamigo, desenvolvida para responder perguntas sobre microfinanças, procedimentos operacionais e políticas do programa. O sistema utiliza tecnologias modernas de IA para:

- 🔍 **Buscar** informações relevantes em documentos técnicos e manuais
- 🧠 **Compreender** perguntas em linguagem natural (português)
- 💬 **Responder** de forma empática, clara e profissional
- 📚 **Citar** as fontes consultadas com scores de relevância
- 🔒 **Garantir** segurança com SSL/TLS configurável

### ✨ Principais Funcionalidades

- **Interface Amigável:** Chat moderno via Streamlit com histórico de conversas
- **Busca Semântica TF-IDF:** Recuperação rápida e eficiente (< 0.01s para 1035 documentos)
- **Citação de Fontes:** Rastreabilidade completa com scores de relevância
- **SSL Flexível:** Suporte a certificados corporativos customizados
- **Logging Completo:** Sistema de logs estruturado para debugging
- **Type Hints:** Código totalmente tipado para melhor manutenibilidade
- **Otimizado:** Dependências reduzidas em 80% (15 pacotes core)

---

## 🏗️ Arquitetura do Sistema

```mermaid
graph TB
    A[📄 Documentos] --> B[🔄 Processamento]
    B --> C[🧮 Embeddings]
    C --> D[🗃️ ChromaDB]
    
    E[👤 Usuário] --> F[💬 Interface Streamlit]
    F --> G[🤖 Agente RAG]
    G --> D
    G --> H[🌐 OpenAI/Azure]
    H --> G
    G --> F
    F --> E
    
    subgraph "Core Components"
        I[📋 Document Loader]
        J[�� Embedding Manager]
        K[🔍 Retriever]
        L[🎯 Agent]
    end
```

### 🔧 Stack Tecnológico

| Componente | Tecnologia | Versão | Função |
|------------|------------|--------|---------|
| **Frontend** | Streamlit | 1.52.0 | Interface de usuário |
| **Framework RAG** | LangChain | 1.1.2 | Orquestração do pipeline |
| **LLM** | OpenAI/Azure | 2.8.1 | Geração de respostas |
| **Vector Store** | ChromaDB | 1.3.5 | Armazenamento de embeddings |
| **Processamento** | Unstructured | 0.18.21 | Extração de texto |
| **Embeddings** | text-embedding-3-small | - | Representação vetorial |

---

## 🚀 Instalação Rápida

### 1. **Pré-requisitos**
```bash
# Python 3.8+ instalado
python --version

# Git (opcional, para clone)
git --version
```

### 2. **Setup Automático**
```bash
# Clone ou baixe o projeto
git clone <repository-url>
cd miamiga-rag

# Execute o setup automático
python setup_project.py

# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# OU
.venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 3. **Configuração Básica**
```bash
# Configure suas credenciais no .env
echo 'OPENAI_API_KEY=sua_chave_aqui' >> .env
echo 'OPENAI_MODEL=gpt-4o-mini' >> .env
```

### 4. **Teste a Instalação**
```bash
python src/core/test_azure_connection.py
```

---

## ⚙️ Configuração

### 📝 Arquivo `.env`

```bash
# === CONFIGURAÇÃO PRINCIPAL ===
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1

# === AZURE OPENAI (Opcional) ===
OPENAI_BASE_URL=https://sua-instancia.openai.azure.com/openai/deployments/modelo/
OPENAI_MODEL=bnb-gpt-4.1-mini

# === CONFIGURAÇÕES AVANÇADAS ===
CHUNK_SIZE=1500
CHUNK_OVERLAP=200
MAX_LOADER_THREADS=4
LOG_LEVEL=INFO

# === PROXY/TLS (Se necessário) ===
REQUESTS_CA_BUNDLE=/caminho/certificado.pem
```

### 🔧 Configurações Disponíveis

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `CHUNK_SIZE` | 1500 | Tamanho dos chunks de texto |
| `CHUNK_OVERLAP` | 200 | Sobreposição entre chunks |
| `LLM_TEMPERATURE` | 0.1 | Criatividade das respostas (0-1) |
| `MAX_LOADER_THREADS` | 4 | Threads para carregamento paralelo |
| `LOG_LEVEL` | INFO | Nível de log (DEBUG, INFO, WARNING) |

---

## 📚 Como Usar

### 1. **Preparar Documentos**

```bash
# Adicione seus documentos na pasta data/docs/
mkdir -p data/docs
cp seus_manuais.pdf data/docs/
cp procedimentos.docx data/docs/
```

**Formatos Suportados:**
- 📕 **PDF** - Manuais, relatórios, documentos
- 📄 **TXT** - Arquivos de texto simples  
- 📘 **DOCX** - Documentos Microsoft Word
- 📊 **PPTX** - Apresentações PowerPoint
- 🌐 **HTML** - Páginas web salvas
- 📝 **MD** - Arquivos Markdown

### 2. **Criar Base de Conhecimento**

```bash
# Processar documentos e criar embeddings
python -c "
from src.miamiga.core.loader import DocumentLoader
from src.miamiga.core.embedding import EmbeddingManager

loader = DocumentLoader()
docs = loader.get_document_chunks()
print(f'📄 Carregados: {len(docs)} chunks')

em = EmbeddingManager()
em.index_documents(docs)
print('✅ Base de conhecimento criada!')
"
```

### 3. **Iniciar o Sistema**

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Iniciar interface
streamlit run app.py
```

### 4. **Interagir com o Sistema**

1. **Acesse:** http://localhost:8501
2. **Digite:** Sua pergunta em português
3. **Aguarde:** Processamento da resposta
4. **Visualize:** Resposta com fontes citadas

**Exemplos de Perguntas:**
- "Quais são os procedimentos de backup do sistema?"
- "Como configurar a autenticação de usuários?"
- "Onde encontro informações sobre políticas de segurança?"

---

## 🧪 Testes e Diagnósticos

### **Scripts de Teste**

```bash
# Teste completo de conectividade
python src/core/test_azure_connection.py

# Verificar dependências instaladas
python scripts/check_imports.py

# Testar processamento de embeddings
python scripts/test_embeddings.py

# Verificar conectividade TLS/HTTPS
python scripts/test_httpx_tls.py

# Testar ChromaDB local
python scripts/test_chroma_local.py
```

### **Health Check do Sistema**

```python
from src.miamiga.core.agent import get_agent

# Verificar status do sistema
agent = get_agent()
health = agent.health_check()
print(health)
```

### **Estatísticas dos Documentos**

```python
from src.miamiga.core.loader import DocumentLoader

loader = DocumentLoader()
chunks = loader.get_document_chunks()
stats = loader.get_chunk_statistics(chunks)

print(f"📊 Total de chunks: {stats['total_chunks']}")
print(f"📏 Tamanho médio: {stats['avg_length']:.0f} caracteres")
print(f"📚 Fontes: {len(stats['sources'])} documentos")
```

---

## 📁 Estrutura do Projeto

```
miamiga-rag/
├── 🎯 app.py                          # Interface Streamlit principal
├── 🎨 styles.css                      # Estilos customizados
├── ⚙️ .env                            # Configurações (criar)
├── 📋 requirements.txt                # Dependências Python
├── 🛠️ setup_project.py               # Setup automático
│
├── �� src/                           # Código fonte
│   ├── 📂 miamiga/core/              # Core refatorado
│   │   ├── 🤖 agent.py               # Agente RAG principal
│   │   ├── 🔗 embedding.py           # Gerenciador de embeddings
│   │   ├── 📄 loader.py              # Carregador de documentos
│   │   └── 🔍 retriever.py           # Recuperador de contexto
│   └── 📂 core/                      # Core legado
│       ├── ⚙️ config.py              # Configurações
│       └── 🔍 retriever.py           # Recuperador de contexto
│
├── 📂 scripts/                       # Scripts utilitários
│   ├── 🔍 check_imports.py           # Diagnóstico de dependências
│   ├── 🧪 test_embeddings.py         # Teste de embeddings
│   └── 🌐 test_httpx_tls.py          # Teste de conectividade
│
├── 📂 data/                          # Dados do sistema
│   ├── 📂 docs/                      # Documentos fonte (criar)
│   └── 📄 knowledge_base.json        # Base de conhecimento (auto)
│
├── �� chroma/                        # Vector store (auto-criado)
└── 📂 .venv/                         # Ambiente virtual (auto-criado)
```

---

## 🛠️ Solução de Problemas

### **Problemas Comuns**

<details>
<summary><strong>❌ Erro: ModuleNotFoundError</strong></summary>

```bash
# Instalar dependências faltantes
pip install langchain-chroma langchain-openai
pip install "unstructured[pdf]"

# Verificar instalação
python scripts/check_imports.py
```
</details>

<details>
<summary><strong>🔌 Erro: Connection timeout</strong></summary>

```bash
# Configurar proxy se necessário
export HTTPS_PROXY=http://proxy:porta
export REQUESTS_CA_BUNDLE=/caminho/certificado.pem

# Testar conectividade
python src/core/test_azure_connection.py
```
</details>

<details>
<summary><strong>�� Erro: Vector store não disponível</strong></summary>

```bash
# Recriar base de conhecimento
rm -rf chroma/
python src/create_vectordb.py

# Verificar documentos
ls -la data/docs/
```
</details>

<details>
<summary><strong>📄 Documentos não carregados</strong></summary>

```bash
# Verificar formatos suportados
python -c "from src.core.config import Config; print(Config.SUPPORTED_EXTENSIONS)"

# Testar carregamento
python -c "from src.miamiga.core.loader import DocumentLoader; loader = DocumentLoader(); docs = loader.get_document_chunks(); print(f'Carregados: {len(docs)} chunks')"
```
</details>

---

## 📊 Performance e Otimização

### **Métricas do Sistema**

| Métrica | Valor Típico | Descrição |
|---------|--------------|-----------|
| **Tempo de Indexação** | ~2-5 docs/seg | Depende do tamanho dos documentos |
| **Tempo de Resposta** | ~3-8 segundos | Inclui busca + geração |
| **Chunks por Documento** | ~10-50 | Baseado no tamanho (1500 chars) |
| **Precisão de Busca** | ~85-95% | Com embeddings de qualidade |

### **Otimizações Recomendadas**

```python
# Para documentos grandes
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 300

# Para respostas mais rápidas
LLM_TEMPERATURE = 0.0
MAX_TOKENS = 500

# Para melhor precisão
RETRIEVAL_K = 6
SCORE_THRESHOLD = 0.7
```

---

## 🔒 Segurança e Privacidade

### **Boas Práticas**

- ✅ **Nunca** commite arquivos `.env` com credenciais
- ✅ **Use** variáveis de ambiente para configurações sensíveis
- ✅ **Mantenha** documentos confidenciais em local seguro
- ✅ **Configure** certificados TLS para ambientes corporativos
- ✅ **Monitore** logs para detectar problemas de acesso

### **Configuração de Proxy Corporativo**

```bash
# Configurar proxy
export HTTP_PROXY=http://proxy.empresa.com:8080
export HTTPS_PROXY=http://proxy.empresa.com:8080
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/empresa.pem

# Testar conectividade
python scripts/test_httpx_tls.py
```

---

## 🚀 Roadmap e Melhorias

### **Versão Atual (1.0)**
- ✅ Interface Streamlit funcional
- ✅ Suporte a múltiplos formatos de documento
- ✅ Integração OpenAI/Azure OpenAI
- ✅ Sistema de busca semântica
- ✅ Scripts de diagnóstico completos

### **Próximas Versões**
- 🔄 **v1.1:** Interface web responsiva
- 🔄 **v1.2:** Suporte a múltiplos idiomas
- 🔄 **v1.3:** API REST para integração
- 🔄 **v1.4:** Dashboard de analytics
- 🔄 **v1.5:** Integração com Active Directory

---

## 🤝 Contribuição

### **Como Contribuir**

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### **Reportar Problemas**

Ao reportar problemas, inclua:
- **Versão** do Python e dependências
- **Logs** de erro completos
- **Passos** para reproduzir o problema
- **Configuração** do ambiente

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

---

## 📞 Suporte

### **Recursos de Ajuda**

- 📚 **Documentação:** [Wiki do Projeto](#)
- 🐛 **Issues:** [GitHub Issues](#)
- 💬 **Discussões:** [GitHub Discussions](#)
- 📧 **Email:** suporte@miamiga-rag.com

### **FAQ Rápido**

**Q: Posso usar com documentos em outros idiomas?**
A: Sim, o sistema suporta múltiplos idiomas, mas funciona melhor em português.

**Q: Qual o limite de documentos?**
A: Não há limite fixo, mas recomenda-se até 1000 documentos para performance ótima.

**Q: Funciona offline?**
A: Não, requer conexão com internet para acessar a API de LLM e embeddings.

---

<div align="center">

**🎉 Pronto para começar? Execute `python setup_project.py` e comece a usar!**

---

*Desenvolvido com ❤️ para facilitar o acesso ao conhecimento corporativo*

</div>


# RAG Chatbot Agent

# 🚀 MiAmiga RAG - Guia Completo de Instalação e Configuração

## 📋 Índice
1. [Visão Geral](#-visão-geral)
2. [Pré-requisitos](#-pré-requisitos)
3. [Instalação](#-instalação)
4. [Configuração](#-configuração)
5. [Preparação dos Documentos](#-preparação-dos-documentos)
6. [Execução](#-execução)
7. [Testes e Diagnósticos](#-testes-e-diagnósticos)
8. [Solução de Problemas](#-solução-de-problemas)
9. [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🎯 Visão Geral

O **MiAmiga RAG** é um sistema de chat inteligente que responde perguntas baseadas em documentos corporativos usando:

- **Frontend:** Interface Streamlit moderna
- **Backend:** LangChain + OpenAI/Azure OpenAI
- **Vector Store:** ChromaDB para busca semântica
- **Processamento:** Suporte a PDF, TXT, DOCX, PPTX, HTML, MD

---

## �� Pré-requisitos

### Sistema
- **Python:** 3.8+ (recomendado 3.10+)
- **Memória:** Mínimo 4GB RAM
- **Espaço:** 2GB livres para dependências

### Acesso à API
- **OpenAI API Key** OU **Azure OpenAI** configurado
- **Conexão com internet** para embeddings

---

## �� Instalação

### 1. **Setup Automático (Recomendado)**

```bash
# Clone ou baixe o projeto
cd miamiga-rag

# Execute o setup automático
python setup_project.py

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 2. **Setup Manual**

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Criar estrutura de pastas
mkdir -p data/docs src/core chroma

# Instalar dependências principais
pip install streamlit langchain langchain-openai langchain-chroma
pip install chromadb unstructured pypdf python-dotenv
pip install langchain-community langchain-text-splitters

# Para processamento avançado de PDFs
pip install "unstructured[pdf]"
```

---

## ⚙️ Configuração

### 1. **Configurar Variáveis de Ambiente**

Crie/edite o arquivo `.env`:

```bash
# === CONFIGURAÇÃO OPENAI/AZURE ===
OPENAI_API_KEY=sua_chave_aqui
OPENAI_BASE_URL=https://sua-instancia.openai.azure.com/openai/deployments/seu-modelo/
OPENAI_MODEL=gpt-4o-mini

# === CONFIGURAÇÕES DO SISTEMA ===
LLM_TEMPERATURE=0.1
CHUNK_SIZE=1500
CHUNK_OVERLAP=200

# === CONFIGURAÇÕES AVANÇADAS ===
MAX_QUESTION_LENGTH=1000
ENABLE_RESPONSE_CACHE=true
CACHE_TTL_SECONDS=3600
MAX_LOADER_THREADS=4
LOG_LEVEL=INFO

# === PROXY/TLS (se necessário) ===
REQUESTS_CA_BUNDLE=/caminho/para/certificado.pem
SSL_CERT_FILE=/caminho/para/certificado.pem
```

### 2. **Configuração para Azure OpenAI (BNB)**

Para uso com Azure OpenAI do Banco do Nordeste:

```bash
OPENAI_API_KEY=sua_chave_azure
OPENAI_BASE_URL=https://bnb-openai.openai.azure.com/openai/deployments/bnb-gpt-4.1-mini/
OPENAI_MODEL=bnb-gpt-4.1-mini
```

### 3. **Teste de Conectividade**

```bash
# Testar conexão Azure OpenAI
python src/core/test_azure_connection.py

# Testar ChromaDB local
python scripts/test_chroma_local.py

# Verificar dependências
python scripts/check_imports.py
```

---

## 📄 Preparação dos Documentos

### 1. **Adicionar Documentos**

```bash
# Copie seus documentos para a pasta data/docs/
cp seus_documentos.pdf data/docs/
cp manual_sistema.docx data/docs/
cp procedimentos.txt data/docs/
```

### 2. **Formatos Suportados**
- ✅ **PDF** - Manuais, relatórios, documentos escaneados
- ✅ **TXT** - Arquivos de texto simples
- ✅ **DOCX** - Documentos Word
- ✅ **PPTX** - Apresentações PowerPoint
- ✅ **HTML** - Páginas web salvas
- ✅ **MD** - Arquivos Markdown

### 3. **Criar Base de Conhecimento**

```bash
# Opção 1: Usando o sistema refatorado (recomendado)
python -c "from src.miamiga.core.loader import DocumentLoader; from src.miamiga.core.embedding import EmbeddingManager; loader = DocumentLoader(); docs = loader.get_document_chunks(); em = EmbeddingManager(); em.index_documents(docs)"

# Opção 2: Usando o script legado
python src/create_vectordb.py
```

---

## 🚀 Execução

### 1. **Iniciar a Interface**

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# OU
.venv\Scripts\activate     # Windows

# Iniciar Streamlit
streamlit run app.py
```

### 2. **Acessar o Sistema**

Abra seu navegador em: **http://localhost:8501**

### 3. **Primeiro Uso**

1. **Aguarde inicialização** (pode levar alguns minutos na primeira vez)
2. **Digite sua pergunta** na caixa de texto
3. **Pressione Enter** ou clique em "Enviar"
4. **Visualize a resposta** com fontes citadas

---

## �� Testes e Diagnósticos

### **Scripts de Teste Disponíveis**

```bash
# 1. Teste completo de conectividade
python src/core/test_azure_connection.py

# 2. Verificar dependências
python scripts/check_imports.py

# 3. Teste de embeddings
python scripts/test_embeddings.py

# 4. Teste TLS/HTTPS
python scripts/test_httpx_tls.py

# 5. Teste ChromaDB local
python scripts/test_chroma_local.py

# 6. Teste do agente RAG
python -c "from src.miamiga.core.agent import main; main()"

# 7. Teste do carregador de documentos
python -c "from src.miamiga.core.loader import main; main()"
```

### **Health Check do Sistema**

```python
from src.miamiga.core.agent import get_agent

agent = get_agent()
health = agent.health_check()
print(health)
```

---

## 🛠️ Solução de Problemas

### **Problema: Erro de Importação**

```bash
# Erro: ModuleNotFoundError
# Solução: Instalar dependências faltantes
pip install langchain-chroma langchain-openai langchain-community

# Para processamento avançado de PDFs
pip install "unstructured[pdf]"
```

### **Problema: Erro de Conectividade**

```bash
# Erro: Connection timeout
# Solução: Verificar proxy/firewall
export HTTPS_PROXY=http://seu-proxy:porta
export HTTP_PROXY=http://seu-proxy:porta

# Configurar certificados
export REQUESTS_CA_BUNDLE=/caminho/para/certificado.pem
```

### **Problema: Vector Store Vazio**

```bash
# Erro: "Vector store não disponível"
# Solução: Recriar base de conhecimento
rm -rf chroma/  # Remove base existente
python src/create_vectordb.py  # Recria base
```

### **Problema: Documentos Não Carregados**

```bash
# Verificar se documentos estão na pasta correta
ls -la data/docs/

# Verificar formatos suportados
python -c "from src.core.config import Config; print(Config.SUPPORTED_EXTENSIONS)"

# Testar carregamento manual
python -c "from src.miamiga.core.loader import DocumentLoader; loader = DocumentLoader(); docs = loader.get_document_chunks(); print(f'Carregados: {len(docs)} chunks')"
```

### **Problema: Inconsistência de Imports**

O projeto tem duas estruturas de imports. Use:

```python
# Para arquivos em src/miamiga/
from miamiga.core.agent import get_agent

# Para arquivos em src/core/
from src.core.config import Config
```

---

## 📁 Estrutura do Projeto

```
miamiga-rag/
├── 📱 app.py                          # Interface Streamlit principal
├── �� styles.css                      # Estilos customizados
├── ⚙️ .env                            # Configurações (criar)
├── �� requirements.txt                # Dependências Python
├── �� setup_project.py               # Setup automático
├── 🧪 test_azure_connection.py       # Teste Azure OpenAI
├── 
├── �� src/
│   ├── 📂 miamiga/core/              # Core refatorado
│   │   ├── 🤖 agent.py               # Agente RAG principal
│   │   ├── 🔗 embedding.py           # Gerenciador embeddings
│   │   ├── 📄 loader.py              # Carregador documentos
│   │   └── 🔍 retriever.py           # Recuperador contexto
│   ├── 📂 core/                      # Core legado
│   │   ├── ⚙️ config.py              # Configurações
│   │   └── 🔍 retriever.py           # Recuperador contexto
│   └── 🗃️ create_vectordb.py         # Criador base conhecimento
├── 
├── �� scripts/                       # Scripts de teste
│   ├── 🔍 check_imports.py           # Diagnóstico dependências
│   ├── 🧪 test_embeddings.py         # Teste embeddings
│   ├── 🌐 test_httpx_tls.py          # Teste conectividade
│   └── 🗃️ test_chroma_local.py       # Teste ChromaDB
├── 
├── 📂 data/
│   ├── 📂 docs/                      # Documentos fonte (criar)
│   └── 📄 knowledge_base.json        # Base conhecimento (auto)
├── 
├── 📂 chroma/                        # Vector store (auto)
└── 📂 .venv/                         # Ambiente virtual (auto)
```

---

## 🎯 Próximos Passos

1. **✅ Configure** as variáveis de ambiente
2. **✅ Adicione** seus documentos em `data/docs/`
3. **✅ Execute** a criação da base de conhecimento
4. **✅ Inicie** a interface com `streamlit run app.py`
5. **✅ Teste** fazendo perguntas sobre seus documentos

---

## 📞 Suporte

Para problemas específicos:

1. **Execute** os scripts de diagnóstico
2. **Verifique** os logs no terminal
3. **Consulte** a seção de solução de problemas
4. **Teste** componentes individualmente

**🎉 Pronto! Seu sistema MiAmiga RAG está configurado e funcionando!**