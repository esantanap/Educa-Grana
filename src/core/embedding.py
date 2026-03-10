# src/IAmiga/core/embedding.py (Versão Refatorada)
import sys
from pathlib import Path

# Adicionar src ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hashlib
import time
from typing import List, Optional, Set
import json

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

from core.config import Config
from core.loader import DocumentLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Exceções personalizadas
class EmbeddingError(Exception):
    pass

class VectorStoreError(Exception):
    pass

class EmbeddingManager:
    """Gerenciador de embeddings e vector store."""
    
    def __init__(self):
        self.embeddings: Optional[OpenAIEmbeddings] = None
        self.vector_store: Optional[Chroma] = None
        self.metrics = EmbeddingMetrics()
        
    def _validate_environment(self) -> None:
        """Valida configurações necessárias."""
        import os
        api_key = os.getenv(Config.OPENAI_ENV_VAR)
        if not api_key:
            raise EmbeddingError(f"{Config.OPENAI_ENV_VAR} não configurado")
            
        if Config.OPENAI_BASE_URL:
            logger.info(f"Usando base URL customizada: {Config.OPENAI_BASE_URL}")
        
        # Criar diretório do Chroma se não existir
        Config.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    
    def initialize_embeddings(self) -> OpenAIEmbeddings:
        """Inicializa cliente de embeddings."""
        self._validate_environment()
        
        try:
            import os
            self.embeddings = OpenAIEmbeddings(
                model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
                openai_api_base=Config.OPENAI_BASE_URL or None,
                openai_api_key=os.getenv(Config.OPENAI_ENV_VAR),
            )
            
            # Teste de conectividade
            _ = self.embeddings.embed_query("teste de conectividade")
            logger.info("✅ Embedding API conectada com sucesso")
            
            return self.embeddings
            
        except Exception as e:
            raise EmbeddingError(f"Falha ao inicializar embeddings: {e}")
    
    def _sanitize_metadata(self, documents: List[Document]) -> List[Document]:
        """Sanitiza metadados para compatibilidade com Chroma."""
        cleaned_documents = []
        
        for doc in documents:
            safe_metadata = {}
            for key, value in doc.metadata.items():
                try:
                    json.dumps(value)  # Testa se é serializável
                    safe_metadata[key] = value
                except (TypeError, ValueError):
                    safe_metadata[key] = str(value)
            
            doc.metadata = safe_metadata
            cleaned_documents.append(doc)
        
        return cleaned_documents
    
    def load_existing_vector_store(self) -> Optional[Chroma]:
        """Carrega vector store existente se disponível."""
        try:
            if not self.embeddings:
                self.initialize_embeddings()
                
            self.vector_store = Chroma(
                persist_directory=str(Config.CHROMA_PATH),
                embedding_function=self.embeddings,
                collection_name="IAmiga_docs",
            )
            
            # Verifica se tem documentos
            collection = self.vector_store._collection
            if collection.count() > 0:
                logger.info(f"Vector store carregado com {collection.count()} documentos")
                return self.vector_store
            else:
                logger.info("Vector store vazio encontrado")
                return None
                
        except Exception as e:
            logger.warning(f"Não foi possível carregar vector store existente: {e}")
            return None
    
    def index_documents(self, documents: List[Document], batch_size: int = 100) -> None:
        """Indexa documentos no vector store."""
        if not documents:
            logger.warning("Nenhum documento fornecido para indexação")
            return
        
        logger.info(f"Iniciando indexação de {len(documents)} documentos")
        self.metrics.start_indexing()
        
        # Sanitizar metadados
        documents = self._sanitize_metadata(documents)
        
        # Inicializar embeddings se necessário
        if not self.embeddings:
            self.initialize_embeddings()
        
        try:
            # Processar em lotes
            total_batches = (len(documents) + batch_size - 1) // batch_size
            
            for i, start_idx in enumerate(range(0, len(documents), batch_size)):
                end_idx = min(start_idx + batch_size, len(documents))
                batch = documents[start_idx:end_idx]
                
                logger.info(f"Processando lote {i+1}/{total_batches} ({len(batch)} documentos)")
                batch_start_time = time.time()
                
                if i == 0 and not self.vector_store:
                    # Primeiro lote - criar vector store
                    self.vector_store = Chroma.from_documents(
                        documents=batch,
                        embedding=self.embeddings,
                        persist_directory=str(Config.CHROMA_PATH),
                        collection_name="IAmiga_docs",
                    )
                else:
                    # Lotes subsequentes - adicionar ao store existente
                    if not self.vector_store:
                        self.vector_store = self.load_existing_vector_store()
                    
                    if self.vector_store:
                        self.vector_store.add_documents(batch)
                    else:
                        raise VectorStoreError("Vector store não disponível")
                
                batch_time = time.time() - batch_start_time
                self.metrics.record_batch(len(batch), batch_time)
                
                logger.info(f"Lote {i+1} processado em {batch_time:.2f}s")
            
            # Persistir mudanças
            if hasattr(self.vector_store, 'persist'):
                self.vector_store.persist()
            
            # Log de métricas finais
            summary = self.metrics.get_summary()
            logger.info(f"✅ Indexação concluída!")
            logger.info(f"📊 Documentos processados: {summary['total_documents']}")
            logger.info(f"⏱️  Tempo total: {summary['total_time_seconds']:.2f}s")
            logger.info(f"🚀 Velocidade: {summary['documents_per_second']:.1f} docs/s")
            
        except Exception as e:
            self.metrics.errors_count += 1
            logger.error(f"Erro durante indexação: {e}")
            raise EmbeddingError(f"Falha na indexação: {e}")
    
    def get_vector_store(self) -> Chroma:
        """Retorna vector store, carregando se necessário."""
        if not self.vector_store:
            self.vector_store = self.load_existing_vector_store()
            
        if not self.vector_store:
            raise VectorStoreError("Vector store não disponível. Execute indexação primeiro.")
            
        return self.vector_store

class EmbeddingMetrics:
    """Coleta métricas de performance da indexação."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.documents_processed: int = 0
        self.errors_count: int = 0
    
    def start_indexing(self):
        self.start_time = time.time()
        self.documents_processed = 0
        self.errors_count = 0
    
    def record_batch(self, batch_size: int, processing_time: float):
        self.documents_processed += batch_size
    
    def get_summary(self) -> dict:
        total_time = time.time() - self.start_time if self.start_time else 0
        return {
            "total_documents": self.documents_processed,
            "total_time_seconds": total_time,
            "documents_per_second": self.documents_processed / total_time if total_time > 0 else 0,
            "errors": self.errors_count,
        }

def main():
    """Função principal para teste do embedding manager."""
    logger.info("=== TESTE DO EMBEDDING MANAGER ===")
    
    try:
        # Carregar documentos
        loader = DocumentLoader()
        documents = loader.get_document_chunks()
        
        if not documents:
            logger.error("Nenhum documento encontrado para indexação")
            return
        
        # Indexar documentos
        embedding_manager = EmbeddingManager()
        embedding_manager.index_documents(documents)
        
        # Testar recuperação
        vector_store = embedding_manager.get_vector_store()
        test_results = vector_store.similarity_search("teste", k=3)
        logger.info(f"Teste de busca retornou {len(test_results)} resultados")
        
    except Exception as e:
        logger.error(f"Erro no teste: {e}")

if __name__ == "__main__":
    main()