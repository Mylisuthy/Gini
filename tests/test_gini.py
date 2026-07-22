import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.router import GiniRouter

try:
    router = GiniRouter()
    res = router.analyze_intent("Necesito agregar un botón verde en el login que diga 'Ingresar'")
    print("Respuesta de Gini:", res)
    
    if os.path.exists("backlog_state.json"):
        with open("backlog_state.json", "r", encoding="utf-8") as f:
            print("\nContenido de backlog_state.json:")
            print(f.read())
    else:
        print("\nNo se creó backlog_state.json")
except Exception as e:
    print("Error:", e)
