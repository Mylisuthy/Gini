import os
import sys
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.state_manager import GlobalStateManager
from src.core.universal_agent import UniversalAgent

load_dotenv()

# Simulate Gini creating the initial backlog record
state_manager = GlobalStateManager()
epic_id = state_manager.init_backlog({
    "tipo_requerimiento": "Nueva Caracteristica",
    "descripcion_original": "Crear un portal de autogestión para los clientes empresariales.",
    "alcance_semantico": "Un portal web seguro donde los clientes corporativos pueden ver sus facturas.",
    "accion_requerida": "Generacion de User Stories y Tareas para Enjambre"
})

print(f"Gini creó el EPIC: {epic_id}")

# Simulate the message passed to Yimi
gini_payload = {
    "epic_id": epic_id,
    "tipo_requerimiento": "Nueva Caracteristica",
    "descripcion_original": "Crear un portal de autogestión para los clientes empresariales.",
    "alcance_semantico": "Un portal web seguro donde los clientes corporativos pueden ver sus facturas.",
    "accion_requerida": "Generacion de User Stories y Tareas para Enjambre"
}

yimi_agent = UniversalAgent('yimi')

print("\n--- Ejecutando Yimi ---")
# Limitamos la generación a algo simple para probar
prompt = json.dumps(gini_payload, indent=2)

# Bypass API call para evitar el error de cuota
data = {
    "azure_backlog": {
        "epic_id": epic_id,
        "iniciativa": {
            "titulo": "Portal Autogestión Empresarial",
            "descripcion": "Crear un portal de autogestión para los clientes empresariales.",
            "fecha_inicio": "2026-07-22T00:00:00Z",
            "fecha_objetivo": "2026-08-22T00:00:00Z",
            "tipo_iniciativa": "Nueva",
            "prioridad": "4"
        },
        "historias": [
            {
                "titulo": "Visualización de Facturas",
                "descripcion": "Como cliente corporativo quiero ver mis facturas.",
                "story_points": 5,
                "tareas": [
                    {
                        "titulo": "Crear endpoint GET /facturas",
                        "descripcion": "Endpoint para obtener la lista de facturas.",
                        "actividad": "Desarrollo",
                        "horas_estimadas": 8
                    }
                ]
            }
        ]
    }
}

print("Ejecutando plan de Yimi simulado...")
execution_logs = yimi_agent.execute_plan(data, prompt)

print("Log de Skills:", str(execution_logs).encode('utf-8', 'replace').decode('utf-8'))

print("\n--- Estado del Blackboard ---")
with open(state_manager.state_file, 'r', encoding='utf-8') as f:
    state_data = json.load(f)
    for record in state_data.get("backlog_activo", []):
        if record.get("id") == epic_id:
            print(f"Estado Actual: {record.get('estado_actual')}")
            print(f"Desglose incluido: {'Sí' if 'desglose' in record else 'No'}")
            if 'desglose' in record:
                desc = json.dumps(record["desglose"], indent=2, ensure_ascii=False)
                print(desc[:300].encode('utf-8', 'replace').decode('utf-8') + "...\n(Truncado)")
