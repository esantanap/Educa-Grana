# src/core/semantic_search.py
import os
import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any, Optional

class IAmigaSemanticSearch:
    """Sistema de busca semântica para IAmiga"""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 cache_dir: str = "./data/embeddings_cache"):
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar modelo
        print(f"🔄 Carregando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Inicializar variáveis
        self.documents = []
        self.embeddings = None
        self.index = None
        self.metadata = []
        
    def _get_cache_path(self) -> Path:
        """Caminho do cache de embeddings"""
        return self.cache_dir / f"embeddings_{self.model_name.replace('/', '_')}.pkl"
    
    def _save_cache(self):
        """Salvar embeddings em cache"""
        cache_data = {
            "documents": self.documents,
            "embeddings": self.embeddings,
            "metadata": self.metadata,
            "model_name": self.model_name
        }
        
        with open(self._get_cache_path(), "wb") as f:
            pickle.dump(cache_data, f)
        
        print(f"💾 Cache salvo: {self._get_cache_path()}")
    
    def _load_cache(self) -> bool:
        """Carregar embeddings do cache"""
        cache_path = self._get_cache_path()
        
        if not cache_path.exists():
            return False
        
        try:
            with open(cache_path, "rb") as f:
                cache_data = pickle.load(f)
            
            if cache_data["model_name"] != self.model_name:
                print("⚠️ Modelo diferente no cache, reprocessando...")
                return False
            
            self.documents = cache_data["documents"]
            self.embeddings = cache_data["embeddings"]
            self.metadata = cache_data["metadata"]
            
            # Recriar índice FAISS
            if self.embeddings is not None:
                self._build_index()
            
            print(f"✅ Cache carregado: {len(self.documents)} documentos")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar cache: {e}")
            return False
    
    def _build_index(self):
        """Construir índice FAISS"""
        if self.embeddings is None:
            return
        
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product
        
        # Normalizar para cosine similarity
        embeddings_normalized = self.embeddings.copy()
        faiss.normalize_L2(embeddings_normalized)
        
        self.index.add(embeddings_normalized)
        print(f"🔍 Índice FAISS criado: {len(self.documents)} documentos, {dimension}D")
    
    def load_knowledge_base(self, knowledge_file: str = "./data/knowledge_base.json"):
        """Carregar base de conhecimento e gerar embeddings"""
        
        # Tentar carregar do cache primeiro
        if self._load_cache():
            return
        
        # Carregar documentos
        if not os.path.exists(knowledge_file):
            print(f"❌ Arquivo não encontrado: {knowledge_file}")
            return
        
        with open(knowledge_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        print(f"📚 Carregando {len(self.documents)} documentos...")
        
        # Extrair textos para embeddings
        texts = []
        self.metadata = []
        
        for i, doc in enumerate(self.documents):
            content = doc.get("content", "")
            source = doc.get("source", f"doc_{i}")
            
            texts.append(content)
            self.metadata.append({
                "source": source,
                "index": i,
                "length": len(content)
            })
        
        # Gerar embeddings
        print("🔄 Gerando embeddings... (pode demorar alguns minutos)")
        self.embeddings = self.model.encode(
            texts, 
            show_progress_bar=True,
            batch_size=32
        )
        
        # Construir índice
        self._build_index()
        
        # Salvar cache
        self._save_cache()
        
        print(f"✅ Sistema pronto! {len(self.documents)} documentos indexados")
    
    def search(self, 
               query: str, 
               top_k: int = 8, 
               min_similarity: float = 0.35) -> List[Dict[str, Any]]:
        """Busca semântica"""
        
        if not self.index:
            print("❌ Sistema não inicializado. Execute load_knowledge_base() primeiro.")
            return []
        
        # Gerar embedding da query
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Buscar no índice
        similarities, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for similarity, idx in zip(similarities[0], indices[0]):
            if similarity >= min_similarity:
                doc = self.documents[idx]
                metadata = self.metadata[idx]
                
                results.append({
                    "content": doc["content"],
                    "source": metadata["source"],
                    "similarity": float(similarity),
                    "metadata": doc,
                    "index": idx
                })
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Estatísticas do sistema"""
        if not self.documents:
            return {"status": "not_loaded"}
        
        return {
            "status": "ready",
            "total_documents": len(self.documents),
            "embedding_dimension": self.embeddings.shape[1] if self.embeddings is not None else 0,
            "model_name": self.model_name,
            "cache_exists": self._get_cache_path().exists()
        }