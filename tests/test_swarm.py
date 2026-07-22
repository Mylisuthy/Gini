import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.universal_agent import UniversalAgent

load_dotenv()

# We will simulate Cami receiving a task
cami_agent = UniversalAgent('cami')

prompt = """
Necesito que implementes una función en Python para calcular el factorial de un número, 
pero quiero que lo delegues a un Micro-Dev para que lo programe, y luego a un Micro-QA para que escriba las pruebas.
Finalmente, tú consolida la solución en un archivo llamado `factorial.py` que contenga ambas cosas.
Usa la etiqueta <crear_enjambre> con este JSON:
[
  {"rol": "Micro-Dev", "tarea": "Escribe la función factorial en Python puro."},
  {"rol": "Micro-QA", "tarea": "Toma la función generada por el Dev y escribe 3 tests usando assert."}
]
"""

print("Iniciando Cami (probando Micro-Enjambres)...")
data = cami_agent.generate_plan(prompt)

if "error" in data:
    print("Error generando plan:", data["error"])
else:
    print("\n--- Plan Generado ---")
    for k, v in data.items():
        if k == "archivos":
            print(f"Archivos ({len(v)}):")
            for a in v:
                print(f"  - {a['nombre']}")
                print(a['contenido'])
        else:
            print(f"{k}: {v}")
