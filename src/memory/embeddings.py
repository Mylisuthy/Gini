import os
from typing import List
from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass
        
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        pass
        
    @property
    @abstractmethod
    def vector_size(self) -> int:
        pass

class GeminiEmbedder(BaseEmbedder):
    def __init__(self):
        import google.generativeai as genai
        from src.core.config_manager import config
        
        api_key = config.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada para usar Embeddings de Google.")
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        import google.generativeai as genai
        result = genai.embed_content(
            model=self.model_name,
            content=texts,
            task_type="retrieval_document"
        )
        return result['embedding']
        
    def embed_query(self, text: str) -> List[float]:
        import google.generativeai as genai
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
        
    @property
    def vector_size(self) -> int:
        return 768  # Tamaño estándar del embedding de Gemini-004

class LocalEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            # Cargamos el modelo (descarga automática la primera vez)
            self.model = SentenceTransformer(model_name)
        except ImportError:
            raise ImportError("Para usar embeddings locales, debes instalar: pip install sentence-transformers torch")
            
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # normalize_embeddings=True ayuda a la similitud del Coseno
        return self.model.encode(texts, normalize_embeddings=True).tolist()
        
    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(text, normalize_embeddings=True).tolist()
        
    @property
    def vector_size(self) -> int:
        # MiniLM tiene 384 dimensiones. BGE-m3 suele tener 1024.
        return self.model.get_sentence_embedding_dimension()

class EmbedderFactory:
    @staticmethod
    def get_embedder() -> BaseEmbedder:
        from src.core.config_manager import config
        # Lee la preferencia del usuario desde la configuración (por defecto 'gemini')
        mode = config.get("EMBEDDING_MODE", "gemini").lower()
        
        if mode == "local":
            return LocalEmbedder()
        else:
            return GeminiEmbedder()
