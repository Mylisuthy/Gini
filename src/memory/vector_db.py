import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from src.memory.embeddings import EmbedderFactory

_qdrant_client_instance = None

class VectorDB:
    def __init__(self, collection_name: str = "gini_knowledge_base"):
        global _qdrant_client_instance
        self.collection_name = collection_name
        
        # Instancia del Embedder Dinámico (Gemini o Local según config)
        self.embedder = EmbedderFactory.get_embedder()
        
        if _qdrant_client_instance is None:
            # Para el entorno masivo y local sin levantar Docker de inmediato,
            # usamos una base de datos Qdrant persistida en archivo.
            qdrant_path = os.path.join(os.path.dirname(__file__), 'qdrant_storage')
            os.makedirs(qdrant_path, exist_ok=True)
            _qdrant_client_instance = QdrantClient(path=qdrant_path)
            
        self.client = _qdrant_client_instance
        
        self._ensure_collection()

    def _ensure_collection(self):
        """Asegura que la colección existe con las dimensiones correctas."""
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedder.vector_size, 
                    distance=Distance.COSINE
                )
            )
            
    def insert_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None):
        """Genera embeddings para fragmentos masivos y los indexa."""
        if not documents:
            return
            
        embeddings = self.embedder.embed_documents(documents)
        
        points = []
        import uuid
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            meta = metadatas[i] if metadatas else {}
            meta['text'] = doc # Guardamos el texto en el payload
            
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=emb,
                    payload=meta
                )
            )
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca los fragmentos más relevantes y retorna su metadata/texto."""
        query_vector = self.embedder.embed_query(query)
        
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )
        
        return [hit.payload for hit in search_result.points]
