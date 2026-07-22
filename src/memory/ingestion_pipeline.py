import os
from typing import List, Dict, Any

class CustomChunker:
    def __init__(self, chunk_size: int = 1500, overlap: int = 300):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def split_text(self, text: str) -> List[str]:
        """Divide el texto en fragmentos con solapamiento (overlap) para no perder semántica."""
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            
            # Ajuste heurístico: intentar no cortar a la mitad de una palabra o frase
            if end < text_len:
                # Retroceder hasta encontrar un espacio o salto de línea
                while end > start and text[end] not in (' ', '\n', '.', ','):
                    end -= 1
                if end == start: # Si la palabra o link es más grande que el chunk entero
                    end = start + self.chunk_size
                    
            chunks.append(text[start:end].strip())
            start = end - self.overlap
            
        return [c for c in chunks if c]

class DocumentParser:
    """Manejador profesional de extracción texto puro para evitar peso de LangChain"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        try:
            import fitz  # PyMuPDF
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text("text") + "\n"
            return text
        except ImportError:
            raise ImportError("Falta dependencia: pip install pymupdf")
            
    @staticmethod
    def parse_docx(file_path: str) -> str:
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except ImportError:
            raise ImportError("Falta dependencia: pip install python-docx")

    @staticmethod
    def parse_text(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

class IngestionPipeline:
    def __init__(self):
        from src.memory.vector_db import VectorDB
        self.db = VectorDB()
        self.chunker = CustomChunker()
        
    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Lee un archivo según su extensión y retorna la lista de metadatos y fragmentos."""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                content = DocumentParser.parse_pdf(file_path)
            elif ext in ['.doc', '.docx']:
                content = DocumentParser.parse_docx(file_path)
            elif ext in ['.txt', '.md', '.csv', '.json', '.xml']:
                content = DocumentParser.parse_text(file_path)
            else:
                print(f"[Ignorado] Formato no soportado: {ext}")
                return []
        except Exception as e:
            print(f"[Error] Falló el parseo de {file_path}: {e}")
            return []
            
        chunks = self.chunker.split_text(content)
        
        records = []
        for i, chunk in enumerate(chunks):
            records.append({
                "text": chunk,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "chunk_index": i,
                    "extension": ext
                }
            })
        return records

    def ingest_directory(self, directory_path: str):
        """Escanea un directorio y carga todos los documentos soportados a Qdrant."""
        if not os.path.exists(directory_path):
            raise ValueError(f"El directorio {directory_path} no existe.")
            
        print(f"Iniciando ingesta masiva desde: {directory_path}")
        
        all_documents = []
        all_metadatas = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Procesando: {file}")
                records = self.process_file(file_path)
                
                for r in records:
                    all_documents.append(r["text"])
                    all_metadatas.append(r["metadata"])
                    
        # Inyectar en Qdrant usando batch (VectorDB Fase 1)
        if all_documents:
            print(f"Inyectando {len(all_documents)} vectores semánticos a Qdrant...")
            self.db.insert_documents(all_documents, all_metadatas)
            print("Ingesta masiva completada exitosamente.")
        else:
            print("No se encontraron documentos válidos para ingestar.")
