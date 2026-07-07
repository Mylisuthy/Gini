import json
from datetime import datetime
from typing import Dict, Any, List

class HandoffProtocol:
    """
    Maneja el protocolo de intercambio de contexto (Handoff) entre los agentes.
    Asegura que la información fluya sin pérdida de contexto.
    """

    @staticmethod
    def create_initial_package(source: str, target: str, original_prompt: str) -> Dict[str, Any]:
        """Crea el sobre inicial generado por Gini."""
        return {
            "metadata": {
                "id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "created_at": datetime.now().isoformat(),
                "status": "in_progress",
                "current_assignee": target
            },
            "context": {
                "original_prompt": original_prompt,
                "history": [
                    {
                        "agent": source,
                        "action": "routed_task",
                        "timestamp": datetime.now().isoformat(),
                        "notes": f"Enrutado a {target}"
                    }
                ]
            },
            "deliverables": {
                "yimi_plan": None,
                "cami_backend": None,
                "fani_frontend": None,
                "mani_qa_report": None
            }
        }

    @staticmethod
    def pass_baton(package: Dict[str, Any], current_agent: str, next_agent: str, deliverable_key: str, deliverable_data: Any, notes: str = "") -> Dict[str, Any]:
        """
        Pasa el paquete al siguiente agente, actualizando el estado y guardando los entregables.
        """
        # 1. Guardar entregable
        if deliverable_key in package["deliverables"]:
            package["deliverables"][deliverable_key] = deliverable_data
        
        # 2. Actualizar el rastro de auditoría
        package["context"]["history"].append({
            "agent": current_agent,
            "action": "completed_task_and_handed_off",
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        })
        
        # 3. Cambiar asignación
        if next_agent.lower() == "done":
            package["metadata"]["status"] = "completed"
            package["metadata"]["current_assignee"] = "None"
        else:
            package["metadata"]["current_assignee"] = next_agent
            
        return package

    @staticmethod
    def render_package(package: Dict[str, Any]) -> str:
        """Renderiza el paquete a JSON estricto."""
        return json.dumps(package, indent=2, ensure_ascii=False)
