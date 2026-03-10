# src/IAmiga/core/loader.py (Versão Refatorada - Conceitual)
import sys
from pathlib import Path

# Adicionar src ao path para imports funcionarem
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os
import logging
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_community.document_loaders import UnstructuredFileLoader, PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from core.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Exceções personalizadas
class DocumentLoadError(Exception):
    pass

class ConfigurationError(Exception):
    pass

class DocumentLoader:
    def __init__(self,
                 data_path: Path = None,
                 supported_extensions: List[str] = None,
                 chunk_size: int = None,
                 chunk_overlap: int = None):
        
        self.data_path = data_path or Config.DATA_PATH
        self.supported_extensions = set(supported_extensions) if supported_extensions else Config.SUPPORTED_EXTENSIONS
        chunk_size = chunk_size or Config.CHUNK_SIZE
        chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
            length_function=len,
            add_start_index=True,
        )

    def _validate_environment(self) -> None:
        if not self.data_path.exists():
            raise ConfigurationError(
                f"Diretório de dados não encontrado: {self.data_path}. "
                f"Crie o diretório e adicione documentos: mkdir -p {self.data_path}"
            )
        
        files = [f for f in self.data_path.rglob("*")
                 if f.is_file() and f.suffix.lower() in self.supported_extensions]
        
        if not files:
            logger.warning(
                f"Nenhum arquivo suportado encontrado em {self.data_path}. "
                f"Formatos suportados: {', '.join(sorted(self.supported_extensions))}"
            )
            raise ConfigurationError("Nenhum arquivo suportado para carregar.")
        
        logger.info(f"Encontrados {len(files)} arquivos suportados no diretório.")

    def _load_single_document(self, file_path: Path) -> List[Document]:
        """Loads a single document, with fallback for PDFs."""
        if file_path.suffix.lower() == ".pdf":
            # Usar PyPDFLoader diretamente (mais estável, evita warnings)
            try:
                loader = PyPDFLoader(str(file_path))
                return loader.load()
            except Exception as e:
                logger.error(f"Falha ao carregar PDF {file_path.name}: {e}")
                raise DocumentLoadError(f"Erro ao carregar {file_path.name}: {e}")
        else:
            try:
                loader = UnstructuredFileLoader(str(file_path), mode="elements")
                return loader.load()
            except Exception as e:
                raise DocumentLoadError(
                    f"Falha ao carregar {file_path.name}: {e}"
                )

    def load_documents(self, show_progress: bool = True) -> List[Document]:
        """
        Carrega todos os documentos do diretório configurado usando multithreading.
        """
        self._validate_environment()
        
        logger.info(f"Carregando documentos de: {self.data_path}")
        
        all_documents: List[Document] = []
        files_to_load = [f for f in self.data_path.rglob("*")
                         if f.is_file() and f.suffix.lower() in self.supported_extensions]
        
        # Using ThreadPoolExecutor for concurrent loading
        max_workers = int(os.getenv("MAX_LOADER_THREADS", "4"))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self._load_single_document, fp): fp
                for fp in files_to_load
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    documents = future.result()
                    all_documents.extend(documents)
                    logger.debug(f"Documento {file_path.name} carregado com sucesso.")
                except DocumentLoadError as e:
                    logger.error(f"Erro ao processar {file_path.name}: {e}")
                except Exception as e:
                    logger.critical(f"Erro inesperado ao carregar {file_path.name}: {e}")

        if not all_documents:
            logger.warning("Nenhum documento foi carregado com sucesso.")
        else:
            logger.info(f"Total de {len(all_documents)} documentos brutos carregados.")
            
        return all_documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Divide documentos em chunks menores para processamento.
        """
        if not documents:
            logger.warning("Nenhum documento fornecido para dividir.")
            return []

        logger.info(f"Dividindo {len(documents)} documentos em chunks...")

        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Divisão concluída: {len(chunks)} chunks criados.")

            if chunks:
                avg_length = sum(len(chunk.page_content) for chunk in chunks) / len(chunks)
                logger.info(f"Tamanho médio dos chunks: {avg_length:.0f} caracteres.")

            return chunks

        except Exception as e:
            logger.error(f"Erro ao dividir documentos: {e}")
            raise DocumentLoadError(f"Falha ao dividir documentos: {e}")

    def get_document_chunks(self) -> List[Document]:
        """
        Orquestra pipeline de carregamento e divisão de documentos.
        """
        logger.info("Iniciando pipeline de processamento de documentos...")

        try:
            raw_documents = self.load_documents()
            chunks = self.split_documents(raw_documents)
            
            if chunks:
                logger.info(f"Pipeline concluído! Total de {len(chunks)} chunks gerados.")
                first_chunk = chunks[0]
                logger.debug(f"\nExemplo do primeiro chunk:")
                logger.debug(f"   Conteúdo: {first_chunk.page_content[:100]}...")
                logger.debug(f"   Fonte: {first_chunk.metadata.get('source', 'N/A')}")
                logger.debug(f"   Página: {first_chunk.metadata.get('page_number', 'N/A')}")
            else:
                logger.warning("Pipeline concluído, mas nenhum chunk foi gerado.")
            
            return chunks
        
        except (DocumentLoadError, ConfigurationError) as e:
            logger.critical(f"Falha no pipeline de documentos: {e}")
            return []
        except Exception as e:
            logger.critical(f"Erro inesperado no pipeline de documentos: {e}")
            return []

    def get_chunk_statistics(self, chunks: List[Document]) -> dict:
        """Gera estatísticas sobre os chunks criados."""
        if not chunks:
            return {}

        lengths = [len(chunk.page_content) for chunk in chunks]

        return {
            "total_chunks": len(chunks),
            "avg_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_characters": sum(lengths),
            "sources": list({chunk.metadata.get("source", "Unknown") for chunk in chunks}),
        }

# Função de teste (main) para ser executada apenas quando o módulo é chamado diretamente
def main() -> None:
    """Função principal para teste do loader."""
    logger.info("=" * 60)
    logger.info("TESTE DO LOADER DE DOCUMENTOS")
    logger.info("=" * 60)

    try:
        loader = DocumentLoader()
        chunks = loader.get_document_chunks()

        if chunks:
            stats = loader.get_chunk_statistics(chunks)
            logger.info(f"\nEstatísticas detalhadas:")
            for key, value in stats.items():
                logger.info(f"   {key}: {value}")
        else:
            logger.warning("\nDicas para solucionar problemas:")
            logger.warning("   1. Verifique se existem arquivos no diretório data/docs/")
            logger.warning("   2. Confirme os formatos suportados: PDF, TXT, DOCX, etc.")
            logger.warning("   3. Execute: pip install 'unstructured[pdf]' para suporte a PDF")
            logger.warning("   4. Verifique permissões de leitura nos arquivos")
    except Exception as e:
        logger.critical(f"Erro no teste principal do loader: {e}")

if __name__ == "__main__":
    main()