# src/agent.py - VERSÃO COM CITAÇÃO DE FONTES + QUERY REWRITE + RERANKING
import sys
from pathlib import Path

# Adicionar src ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).resolve().parent))

import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import logging

# Importar módulos de query rewrite e reranking
from core.search.query_rewriter import QueryRewriter
from core.search.reranker import heuristic_rerank

# Importar guardrails
from core.guardrails.input_filter import validate_user_input
from core.guardrails.output_filter import OutputGuardrails

# Importar XAI logger
from core.xai.explainer import xai_logger
from core.xai.counterfactuals import counterfactual_generator

load_dotenv(override=True)

# Configurar logger com FileHandler
log_dir = Path(__file__).parent.parent / "data"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def configure_ssl_flexible() -> Optional[str]:
    """Configurar SSL de forma flexível usando variáveis de ambiente
    
    Returns:
        Optional[str]: Path do certificado se encontrado, None caso contrário
    """
    # Tentar obter certificado das variáveis de ambiente
    cert_path = os.getenv('REQUESTS_CA_BUNDLE') or os.getenv('SSL_CERT_FILE')
    
    if cert_path and os.path.exists(cert_path):
        # Garantir que todas as variáveis estejam configuradas
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['CURL_CA_BUNDLE'] = cert_path
        os.environ['SSL_CERT_FILE'] = cert_path
        logger.info(f"[SSL] Certificados SSL configurados: {cert_path}")
        return cert_path
    else:
        logger.warning("[SSL] Certificado SSL não encontrado. Configure REQUESTS_CA_BUNDLE ou SSL_CERT_FILE no .env")
        return None

def make_api_request_flexible(
    url: str, 
    payload: Dict[str, Any], 
    headers: Dict[str, str], 
    timeout: int = 60
) -> requests.Response:
    """Fazer requisição API com SSL seguro
    
    Args:
        url: URL da API
        payload: Dados da requisição
        headers: Headers HTTP
        timeout: Timeout em segundos
        
    Returns:
        Response object
        
    Raises:
        requests.exceptions.RequestException: Se todas as tentativas falharem
    """
    # Obter certificado das variáveis de ambiente
    cert_path = os.getenv('REQUESTS_CA_BUNDLE') or os.getenv('SSL_CERT_FILE')
    allow_insecure = os.getenv('ALLOW_INSECURE_SSL', 'false').lower() == 'true'
    
    # Para APIs Azure, preferir certificados do sistema
    is_azure_url = 'azurecontainerapps.io' in url or 'azure' in url.lower()
    
    # Configurações SSL (ordem de preferência)
    ssl_configs = []
    
    if is_azure_url:
        # Para Azure: tentar primeiro certificados do sistema
        ssl_configs.append((True, "certificados do sistema"))
        if cert_path and os.path.exists(cert_path):
            ssl_configs.append((cert_path, "certificado corporativo"))
    else:
        # Para outras URLs: tentar primeiro certificado customizado
        if cert_path and os.path.exists(cert_path):
            ssl_configs.append((cert_path, "certificado corporativo"))
        ssl_configs.append((True, "certificados do sistema"))
    
    # Adicionar opção insegura APENAS se explicitamente permitido
    if allow_insecure:
        ssl_configs.append((False, "SSL inseguro"))
        # Warning apenas na primeira vez
        if not hasattr(make_api_request_flexible, '_insecure_warned'):
            logger.warning("[API] ⚠️ ALLOW_INSECURE_SSL=true detectado. Desabilite para produção!")
            make_api_request_flexible._insecure_warned = True
    
    
    last_error = None
    successful_method = None
    
    for i, (verify_setting, description) in enumerate(ssl_configs, 1):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout,
                verify=verify_setting
            )
            
            if response.status_code == 200:
                # Sucesso - log apenas na primeira requisição de cada sessão
                if not successful_method or successful_method != description:
                    logger.info(f"[API] ✓ Conectado via {description}")
                    successful_method = description
                return response
            else:
                last_error = f"HTTP {response.status_code}"
                
        except requests.exceptions.SSLError as e:
            last_error = "Erro SSL"
            continue
        except requests.exceptions.RequestException as e:
            last_error = "Erro de conexão"
            continue
    
    error_msg = (
        f"Todas as {len(ssl_configs)} configurações SSL falharam.\n"
        f"Último erro: {last_error}\n\n"
        f"💡 Dica: Se estiver usando certificado corporativo:\n"
        f"   1. Verifique se REQUESTS_CA_BUNDLE está correto no .env\n"
        f"   2. Para ambiente de desenvolvimento, adicione ALLOW_INSECURE_SSL=true no .env"
    )
    raise requests.exceptions.RequestException(error_msg)

# Configurar SSL
configure_ssl_flexible()

# Inicializar Query Rewriter
REWRITER = QueryRewriter(glossario_path="src/core/domain/glossario.json")
logger.info("[SYSTEM] Query Rewriter inicializado com glossario")

# Inicializar Output Guardrails
OUTPUT_GUARDRAILS = OutputGuardrails()
logger.info("[SYSTEM] Guardrails de saída inicializados")

logger.info("[SYSTEM] Persona temporariamente desabilitada para evitar erro de null bytes")
logger.info("[SYSTEM] Busca Semantica Local disponivel (TF-IDF)")

class LocalSemanticSearchEngine:
    """Motor de busca semântica usando TF-IDF com logs detalhados"""
    
    def __init__(self):
        self.vectorizer = None
        self.document_vectors = None
        self.documents = []
        self.initialized = False
        logger.debug("[ENGINE] LocalSemanticSearchEngine inicializado")
        
    def initialize(self, knowledge_base: List[Dict]) -> bool:
        """Inicializar sistema de busca semântica local"""
        if self.initialized:
            logger.debug("[ENGINE] Sistema TF-IDF ja inicializado")
            return True
        
        try:
            self.documents = knowledge_base
            
            logger.info(f"[ENGINE] Criando indice TF-IDF para {len(knowledge_base)} documentos...")
            
            texts = [doc.get("content", "") for doc in knowledge_base]
            
            self.vectorizer = TfidfVectorizer(
                max_features=10000,  # 🔥 Dobrado para capturar mais termos
                ngram_range=(1, 3),  # 🔥 Trigramas para frases mais complexas
                lowercase=True,
                min_df=1,
                max_df=0.85,  # 🔥 Reduzido para evitar termos muito genéricos
                sublinear_tf=True  # 🔥 Normalização logarítmica (melhora qualidade)
            )
            
            start_time = time.time()
            self.document_vectors = self.vectorizer.fit_transform(texts)
            end_time = time.time()
            
            self.initialized = True
            logger.info(f"[ENGINE] Sistema TF-IDF inicializado! Vetores: {self.document_vectors.shape}")
            logger.info(f"[ENGINE] Tempo de inicializacao: {end_time - start_time:.2f}s")
            return True
            
        except Exception as e:
            logger.error(f"[ENGINE] Erro ao inicializar TF-IDF: {e}")
            return False
    
    def search(self, query: str, top_k: int = 12, min_similarity: float = 0.10) -> List[Tuple[float, Dict]]:
        """Busca semântica usando TF-IDF
        
        Args:
            query: Consulta do usuário
            top_k: Número máximo de resultados (otimizado para 12)
            min_similarity: Threshold mínimo (otimizado para 0.10 - melhor recall)
        """
        if not self.initialized:
            logger.error("[ENGINE] Sistema TF-IDF nao inicializado")
            return []
        
        try:
            logger.debug(f"[ENGINE] Executando busca TF-IDF para: '{query}'")
            
            start_time = time.time()
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
            top_indices = similarities.argsort()[-top_k:][::-1]
            end_time = time.time()
            
            results = []
            for idx in top_indices:
                similarity = similarities[idx]
                if similarity >= min_similarity:
                    results.append((float(similarity), self.documents[idx]))
            
            logger.info(f"[ENGINE] Busca TF-IDF: {len(results)} resultados em {end_time - start_time:.3f}s")
            
            for i, (score, doc) in enumerate(results, 1):
                source = doc.get('source', 'N/A')[:50]
                logger.debug(f"  [ENGINE] {i}. Score: {score:.3f} - {source}...")
            
            return results
            
        except Exception as e:
            logger.error(f"[ENGINE] Erro na busca TF-IDF: {e}")
            return []

# Instância global
_semantic_engine = None

def get_semantic_engine() -> Optional[LocalSemanticSearchEngine]:
    """Obter instância do motor semântico"""
    global _semantic_engine
    if _semantic_engine is None:
        logger.debug("[ENGINE] Criando nova instancia do motor semantico")
        _semantic_engine = LocalSemanticSearchEngine()
    return _semantic_engine

def load_knowledge_base() -> List[Dict[str, Any]]:
    """Carregar base de conhecimento com logs
    
    Returns:
        List[Dict[str, Any]]: Lista de documentos da base de conhecimento
    """
    # Detectar caminho relativo ao arquivo atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_file = os.path.join(current_dir, "..", "data", "knowledge_base.json")
    
    logger.debug(f"[KB] Tentando carregar base de: {knowledge_file}")
    
    if not os.path.exists(knowledge_file):
        logger.error("[KB] Base de conhecimento nao encontrada!")
        return []
    
    try:
        with open(knowledge_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        logger.info(f"[KB] Base carregada: {len(data)} documentos")
        return data
    except Exception as e:
        logger.error(f"[KB] Erro ao carregar base: {e}")
        return []

def search_knowledge_semantic(
    query: str, 
    knowledge_base: List[Dict[str, Any]], 
    max_results: int = 5
) -> List[Tuple[float, Dict[str, Any]]]:
    """Busca semântica usando TF-IDF com logs
    
    Args:
        query: Pergunta do usuário
        knowledge_base: Base de conhecimento
        max_results: Número máximo de resultados
        
    Returns:
        List[Tuple[float, Dict[str, Any]]]: Lista de tuplas (score, documento)
    """
    logger.info(f"[SEARCH] INICIANDO BUSCA SEMANTICA para: '{query}'")
    
    semantic_engine = get_semantic_engine()
    
    if not semantic_engine:
        logger.error("[SEARCH] Motor semantico nao disponivel")
        return []
    
    if not semantic_engine.initialized:
        logger.info("[SEARCH] Inicializando busca semantica...")
        if not semantic_engine.initialize(knowledge_base):
            logger.error("[SEARCH] Falha na inicializacao")
            return []
    
    semantic_results = semantic_engine.search(query, top_k=max_results, min_similarity=0.10)
    
    if semantic_results:
        logger.info(f"[SEARCH] Busca semantica concluida: {len(semantic_results)} resultados")
        return [(score, doc) for score, doc in semantic_results]
    else:
        logger.warning("[SEARCH] Busca semantica sem resultados")
        return []

def search_knowledge_keyword(
    query: str, 
    knowledge_base: List[Dict[str, Any]], 
    max_results: int = 3
) -> List[Tuple[int, Dict[str, Any]]]:
    """Busca simples por palavras-chave com logs
    
    Args:
        query: Pergunta do usuário
        knowledge_base: Base de conhecimento
        max_results: Número máximo de resultados
        
    Returns:
        List[Tuple[int, Dict[str, Any]]]: Lista de tuplas (score, documento)
    """
    logger.info(f"[SEARCH] BUSCA POR PALAVRAS-CHAVE para: '{query}'")
    
    query_lower = query.lower()
    results = []
    
    for item in knowledge_base:
        content_lower = item["content"].lower()
        
        score = 0
        for word in query_lower.split():
            if len(word) > 2:
                if word in content_lower:
                    score += content_lower.count(word)
        
        if score > 0:
            results.append((score, item))
    
    results.sort(key=lambda x: x[0], reverse=True)
    final_results = [(score, item) for score, item in results[:max_results]]
    
    logger.info(f"[SEARCH] Busca por palavras-chave: {len(final_results)} resultados")
    
    return final_results

def format_sources_section(relevant_docs_with_scores: List[Tuple[float, Dict[str, Any]]]) -> str:
    """🆕 Formatar seção de fontes - SEM DUPLICATAS e melhor apresentação
    
    Args:
        relevant_docs_with_scores: Lista de tuplas (score, documento)
        
    Returns:
        str: Seção formatada de fontes ou string vazia
    """
    if not relevant_docs_with_scores:
        return ""
    
    # Agrupar por fonte para evitar duplicatas
    sources_dict = {}
    for score, doc in relevant_docs_with_scores:
        source_name = doc.get('source', 'Documento não identificado')
        
        # Limpar nome da fonte
        source_name = source_name.strip()
        if not source_name:
            source_name = 'Documento não identificado'
        
        if source_name not in sources_dict:
            sources_dict[source_name] = score
        else:
            # Manter o MAIOR score se fonte duplicada
            sources_dict[source_name] = max(sources_dict[source_name], score)
    
    # Se não há fontes válidas
    if not sources_dict:
        return ""
    
    sources_section = "\n\n📚 **Fontes consultadas:**\n"
    
    # Ordenar por relevância (maior para menor) e limitar a 5
    sorted_sources = sorted(sources_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for i, (source_name, score) in enumerate(sorted_sources, 1):
        # Limitar nome da fonte se muito longo
        if len(source_name) > 70:
            source_name = source_name[:67] + "..."
        
        # Formatação melhorada com numeração
        sources_section += f"{i}. **{source_name}** (relevância: {score:.2f})\n"
    
    return sources_section

def format_IAmiga_response(response: str, sources_section: str = "") -> str:
    """🆕 Aplicar formatação da IAmiga com seção de fontes
    
    Args:
        response: Resposta base
        sources_section: Seção de fontes formatada
        
    Returns:
        str: Resposta formatada completa
    """
    logger.debug("[FORMAT] Aplicando formatacao IAmiga com fontes")
    
    # Verificar se já tem assinatura IAmiga
    has_signature = any(marker in response for marker in ["🤖 **IAmiga**", "🤖 IAmiga", "Assistente Virtual do Educa Grana"])
    
    # Se já tem assinatura, apenas adiciona fontes se necessário
    if has_signature:
        if sources_section and sources_section not in response:
            # Inserir fontes antes da última assinatura
            if "🤖" in response:
                parts = response.rsplit("🤖", 1)
                response = parts[0] + sources_section + "\n\n🤖" + parts[1]
            else:
                response += sources_section
        return response
    
    # Adicionar saudação se necessário
    if not any(word in response.lower() for word in ["olá", "oi", "bom dia"]):
        response = "😊 Olá! " + response
    
    # Adicionar fontes
    if sources_section:
        response += sources_section
    
    # Adicionar assinatura apenas se não existir
    response += "\n\n🤖 **IAmiga** - Assistente Virtual do Educa Grana"
    
    return response

def answer_question(question: str) -> str:
    """🆕 Responder pergunta usando busca semântica + API com citação de fontes
    
    Args:
        question: Pergunta do usuário
        
    Returns:
        str: Resposta formatada com fontes
        
    Raises:
        Exception: Se houver erro no processamento
    """
    logger.info(f"\n[AGENT] PROCESSANDO PERGUNTA: '{question}'")
    logger.info("=" * 80)
    
    # 🛡️ GUARDRAIL DE ENTRADA - Validar pergunta
    is_valid_input, error_message = validate_user_input(question)
    if not is_valid_input:
        logger.warning(f"[GUARDRAIL] Pergunta bloqueada: {error_message}")
        
        # 🔍 XAI: Log de guardrails
        xai_logger.log_guardrails(
            passed=False,
            violations=[{"type": "input_validation", "severity": "critical", "message": error_message}],
            query=question,
            explanation=f"Query bloqueada por: {error_message}"
        )
        
        return f"🛡️ **Conteúdo bloqueado**: {error_message}\n\n" + \
               "Por favor, faça perguntas relacionadas ao Educa Grana e serviços do BNB."
    
    try:
        knowledge_base = load_knowledge_base()
        if not knowledge_base:
            error_msg = "Base de conhecimento não disponível."
            logger.error("[AGENT] Base de conhecimento vazia")
            return format_IAmiga_response(error_msg)
        
        # 1) Reescrever consulta com expansão de sinônimos
        expanded_query, added_terms = REWRITER.rewrite(question)
        if added_terms:
            logger.info(f"[REWRITE] '{question}' -> '{expanded_query}' | Adicionados: {added_terms}")
            
            # 🔍 XAI: Log de query rewrite
            xai_logger.log_query_rewrite(
                original_query=question,
                rewritten_query=expanded_query,
                added_terms=added_terms,
                explanation=f"Query expandida com {len(added_terms)} sinônimos para melhorar recuperação"
            )
        else:
            logger.info(f"[REWRITE] Query sem expansão: '{question}'")
        
        # 2) Buscar com TF-IDF usando query expandida
        relevant_docs_with_scores = search_knowledge_semantic(expanded_query, knowledge_base, max_results=12)
        search_type = "semântica"
        
        # Se busca semântica falhar, usar busca por palavras-chave
        if not relevant_docs_with_scores:
            logger.warning("[AGENT] Fallback para busca por palavras-chave")
            relevant_docs_with_scores = search_knowledge_keyword(expanded_query, knowledge_base, max_results=6)
            search_type = "palavras-chave"
        
        if not relevant_docs_with_scores:
            no_info_msg = "Não encontrei informações específicas para sua pergunta."
            logger.warning("[AGENT] Nenhum documento relevante encontrado")
            return format_IAmiga_response(no_info_msg)
        
        logger.info(f"[AGENT] Documentos relevantes encontrados: {len(relevant_docs_with_scores)} (busca {search_type})")
        
        # 🔍 XAI: Log de document retrieval
        docs_for_xai = [
            {
                'score': score,
                'snippet': doc.get('content', '')[:200],
                'matched_terms': []  # Pode adicionar lógica para detectar termos matched
            }
            for score, doc in relevant_docs_with_scores
        ]
        xai_logger.log_document_retrieval(
            query=expanded_query,
            retrieved_docs=docs_for_xai,
            total_docs=len(knowledge_base),
            explanation=f"Busca {search_type} retornou {len(relevant_docs_with_scores)} documentos relevantes"
        )
        
        # 3) Re-ranking heurístico dos documentos
        # Converter para formato esperado pelo reranker
        docs_for_rerank = [{"score": score, **doc} for score, doc in relevant_docs_with_scores]
        reranked_docs = heuristic_rerank(expanded_query, docs_for_rerank)
        
        # Converter de volta para tuplas (score, doc)
        relevant_docs_with_scores = [(d.pop("score"), d) for d in reranked_docs]
        logger.info(f"[RERANK] Documentos re-ranqueados com heurísticas")
        
        # Montar contexto apenas com o conteúdo
        context = "\n\n".join([doc["content"] for score, doc in relevant_docs_with_scores])
        
        # 🆕 Gerar seção de fontes
        sources_section = format_sources_section(relevant_docs_with_scores)
        
        prompt = f"""Você é a AiAmiga, assistente virtual do Educa Grana (BNB). Seja AMIGÁVEL, ACOLHEDORA, HUMANA e CONCISA.

Contexto:
{context}

Pergunta: {question}

INSTRUÇÕES DE COMUNICAÇÃO:
- Responda de forma BREVE e DIRETA - máximo 3-4 parágrafos curtos
- Use linguagem NATURAL e ACOLHEDORA, como uma amiga que está ajudando
- Comece com cumprimento caloroso (😊 Olá! Que bom te ver aqui!, Oi! Fico feliz em ajudar!)
- Use emojis COM MODERAÇÃO para transmitir calor humano (máximo 2-3 por resposta)
- Seja empática e demonstre interesse genuíno pela situação do cliente
- Termine oferecendo ajuda de forma cordial: "Estou aqui se precisar de mais alguma coisa!" ou similar

INSTRUÇÕES DE CONTEÚDO:
- Liste itens de forma CLARA e ORGANIZADA (use bullet points quando facilitar a compreensão)
- Responda APENAS o que foi perguntado, mas com gentileza
- Se houver muitas opções, organize de forma amigável e fácil de entender
- Use APENAS o contexto fornecido
- Quando houver problemas ou limitações, seja empática e sugira alternativas: "Entendo sua situação. O ideal seria conversar com seu Agente/Coordenador que poderá ajudar melhor."

TOM E PERSONALIDADE:
- Demonstre interesse genuíno pelas necessidades do cliente
- Use frases como: "Vou te explicar...", "Fico feliz em esclarecer...", "Entendo sua dúvida..."
- Evite ser robótica - seja natural e humana

IMPORTANTE sobre linhas de crédito:
- Linhas: Giro Solidário, Giro Individual, Investimento Fixo, Educa Grana Comunidade, Educa Grana Mais, Educa Grana Delas
- NÃO são linhas: Seguro Vida, Seguro Prestamista, Maquininha, Soluções Digitais"""
        
        logger.info("[AGENT] Chamando API...")
        
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("OPENAI_MODEL", "bnb-gpt-4.1-mini")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200,
            "temperature": 0.1
        }
        
        response = make_api_request_flexible(
            f"{base_url}/chat/completions",
            payload,
            headers
        )
        
        if response.status_code == 200:
            data = response.json()
            raw_answer = data['choices'][0]['message']['content']
            
            logger.info("[AGENT] Resposta gerada com sucesso!")
            
            # Adicionar fontes à resposta (sem formatação extra)
            if sources_section:
                final_response = raw_answer + sources_section
            else:
                final_response = raw_answer
            
            logger.info(f"[AGENT] Resposta final: {len(final_response)} caracteres")
            
            # � XAI: Log de confidence score
            avg_score = sum(score for score, _ in relevant_docs_with_scores[:5]) / min(5, len(relevant_docs_with_scores))
            confidence = min(avg_score, 1.0)  # Normalizar para 0-1
            
            xai_logger.log_confidence_score(
                confidence=confidence,
                factors={
                    'doc_scores': avg_score,
                    'num_docs': len(relevant_docs_with_scores),
                    'search_type': search_type,
                    'query_expanded': len(added_terms) > 0
                },
                explanation=f"Confiança baseada em {len(relevant_docs_with_scores)} documentos com score médio {avg_score:.3f}"
            )
            
            # 🔍 XAI: Log de citations
            citations = [
                {
                    'source': doc.get('source', 'Desconhecido'),
                    'text': doc.get('content', '')[:100]
                }
                for _, doc in relevant_docs_with_scores[:3]
            ]
            xai_logger.log_citation(
                citations=citations,
                explanation=f"Resposta baseada em {len(citations)} fontes principais"
            )
            
            # 🛡️ GUARDRAIL DE SAÍDA - Validar resposta
            is_valid_output, processed_response = OUTPUT_GUARDRAILS.validate_response(final_response, question)
            if not is_valid_output:
                logger.warning("[GUARDRAIL] Resposta bloqueada por conter conteúdo inadequado")
                processed_response = OUTPUT_GUARDRAILS._get_safe_fallback_response()
            else:
                # 🔍 XAI: Log de guardrails passando
                xai_logger.log_guardrails(
                    passed=True,
                    violations=[],
                    query=question,
                    explanation="Resposta passou em todas as validações de segurança"
                )
            
            # 🔍 XAI: Gerar e logar counterfactuals
            try:
                counterfactuals = counterfactual_generator.generate_counterfactuals(
                    original_query=question,
                    num_results=len(relevant_docs_with_scores),
                    added_terms=added_terms
                )
                
                if counterfactuals:
                    xai_logger.log_counterfactual(
                        counterfactuals=counterfactuals,
                        query=question,
                        explanation=f"Gerados {len(counterfactuals)} cenários 'E se...?' para análise"
                    )
                    logger.info(f"[XAI] Counterfactuals gerados: {len(counterfactuals)}")
            except Exception as e:
                logger.debug(f"[XAI] Erro ao gerar counterfactuals: {e}")
            
            # 4) Telemetria básica (opcional)
            try:
                telemetry_data = {
                    "event": "query_rewrite_rerank",
                    "original_query": question,
                    "expanded_query": expanded_query,
                    "added_terms": added_terms,
                    "num_results": len(relevant_docs_with_scores),
                    "search_type": search_type
                }
                with open("data/telemetry.log", "a", encoding="utf-8") as f:
                    f.write(json.dumps(telemetry_data) + "\n")
            except Exception as e:
                logger.debug(f"[TELEMETRY] Falha ao gravar telemetria: {e}")
            
            return processed_response
        else:
            error_msg = f"Erro na API: {response.status_code}"
            logger.error(f"[AGENT] Erro na API: {response.status_code}")
            return format_IAmiga_response(error_msg)
        
    except Exception as e:
        error_msg = f"Problema técnico: {str(e)}"
        logger.error(f"[AGENT] Erro na execucao: {e}")
        return format_IAmiga_response(error_msg)

# ============================================================================
# TESTE
# ============================================================================
if __name__ == "__main__":
    # Configurar encoding para Windows
    import sys
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    logger.info("=" * 70)
    logger.info("TESTANDO AGENT COM CITACAO DE FONTES")
    logger.info("=" * 70)
    
    response = answer_question("O que é o Educa Grana?")
    logger.info(f"\nResposta Final:\n{response}")
    
    logger.info("\nAgent com citacao de fontes funcionando!")