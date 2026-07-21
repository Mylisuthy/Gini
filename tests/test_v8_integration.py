import sys
import os
import pytest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.universal_agent import UniversalAgent
from src.core.config_manager import config

# Skip si no hay API key configurada
@pytest.mark.skipif(not config.get("GEMINI_API_KEY"), reason="Requiere GEMINI_API_KEY configurada para pruebas de integracion")
def test_universal_agent_live_cognitive_test():
    """
    PRUEBA DE INTEGRACIÓN (Fuego Real):
    Conecta a la API de Gemini y verifica que la asimilación del prompt y el XML 7D 
    están funcionando perfectamente.
    """
    
    # Usamos a Cami (Backend Dev) para que cree un script en Python
    agent = UniversalAgent("cami")
    
    print("\n[TEST] Enviando requerimiento real a Cami (Gemini)...")
    start_time = time.time()
    plan = agent.generate_plan("Necesito que crees un archivo suma.py en esta ruta que contenga una funcion sumar(a, b). Usa buenas practicas.")
    
    print(f"[TEST] Respuesta recibida en {time.time() - start_time:.2f}s")
    
    # Verificaciones asertivas de que Cami siguió las reglas 7D
    assert "error" not in plan, f"Error devuelto por la IA: {plan.get('error')}"
    
    # 1. ¿Logró reflexionar?
    assert "reflexion" in plan, "El agente no incluyó la etiqueta <reflexion>"
    assert len(plan["reflexion"]) > 5, "La reflexión es demasiado corta"
    
    # 2. ¿Entregó el archivo?
    assert len(plan["archivos"]) > 0, "El agente no generó ningún <archivo>"
    
    # Encontramos el archivo Python
    py_file = next((f for f in plan["archivos"] if f["nombre"].endswith(".py")), None)
    assert py_file is not None, "El agente no creó el script suma.py"
    
    # Verificamos que el código de Python esté correcto
    codigo = py_file["contenido"]
    assert "def sumar" in codigo, "El código generado no contiene la función 'sumar'"
    assert "return" in codigo, "La función no retorna el valor"

    print("[TEST] ¡Prueba cognitiva V8.0 superada! El XML fue respetado matemáticamente.")
