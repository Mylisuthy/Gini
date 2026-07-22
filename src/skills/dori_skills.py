def get_skills():
    return [
        "diagram_generation",
        "technical_writing",
        "rag_ingestion"
    ]

def execute_skills(data: dict) -> list:
    log = []
    
    if "ingestar_conocimiento" in data:
        directorio = data["ingestar_conocimiento"]
        try:
            from src.memory.ingestion_pipeline import IngestionPipeline
            pipeline = IngestionPipeline()
            pipeline.ingest_directory(directorio)
            log.append(f"Ingesta masiva RAG completada para el directorio: {directorio}")
        except Exception as e:
            log.append(f"Error en ingesta RAG para el directorio {directorio}: {str(e)}")
            
    return log
