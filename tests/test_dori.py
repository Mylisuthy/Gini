import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.universal_agent import UniversalAgent

dori = UniversalAgent("dori")

print("--- FASE 1: Solicitud de Ingesta ---")
prompt_ingesta = f"Dori, por favor ingesta la documentación del directorio {os.path.abspath('Pruebas/rag_test')} en la base vectorial."
plan = dori.generate_plan(prompt_ingesta)
print("Plan generado:", plan)

if "ingestar_conocimiento" in plan:
    resultado = dori.execute_plan(plan, prompt_ingesta)
    print("\nResultado ejecución:", resultado)

print("\n--- FASE 2: Búsqueda RAG Autónoma ---")
prompt_busqueda = "Dori, ¿Cuál es el código del protocolo principal según la directriz de Celsia? Usa la base vectorial para investigar y responde usando RAG."
# Al procesar generate_plan, Dori debería usar <buscar_rag>
plan2 = dori.generate_plan(prompt_busqueda)
print("Plan generado 2:", plan2)

