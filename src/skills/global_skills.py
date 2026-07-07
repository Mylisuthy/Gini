# Global Skills
# Herramientas compartidas que cualquier agente puede utilizar.

def read_file(filepath: str) -> str:
    """Lee el contenido de un archivo en el disco."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo archivo: {e}"

def write_file(filepath: str, content: str) -> bool:
    """Escribe contenido en un archivo del disco."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error escribiendo archivo: {e}")
        return False

def format_json_output(data: dict) -> str:
    """Asegura que el formato de salida sea un JSON válido (útil para Handoff)."""
    import json
    return json.dumps(data, indent=2, ensure_ascii=False)
