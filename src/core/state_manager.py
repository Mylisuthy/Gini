import os
import json
from datetime import datetime

class GlobalStateManager:
    def __init__(self, root_dir=None):
        if root_dir is None:
            # Asumiendo que este archivo está en src/core/
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        else:
            self.root_dir = root_dir
            
        self.state_file = os.path.join(self.root_dir, 'backlog_state.json')

    def init_backlog(self, payload: dict) -> str:
        """
        Inicializa o actualiza el archivo backlog_state.json creando un nuevo 
        registro maestro en estado BACKLOG a partir del payload enviado por Gini.
        """
        record = {
            "id": "EPIC-001",
            "timestamp": datetime.now().isoformat(),
            "estado_actual": "BACKLOG",
            "detalles": payload
        }
        
        state_data = {
            "historico": [],
            "backlog_activo": [record]
        }
        
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                if "backlog_activo" not in state_data:
                    state_data["backlog_activo"] = []
                if "historico" not in state_data:
                    state_data["historico"] = []
                    
                # Generar ID consecutivo
                total_records = len(state_data["backlog_activo"]) + len(state_data["historico"])
                record["id"] = f"EPIC-{total_records + 1:03d}"
                
                state_data["backlog_activo"].append(record)
            except Exception:
                pass # Si el archivo está corrupto, se sobreescribe con el nuevo state_data
                
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=4, ensure_ascii=False)
            
        return record["id"]

    def update_epic_with_breakdown(self, epic_id: str, breakdown: dict) -> bool:
        """
        Busca un epic por su id en backlog_activo, le inyecta el desglose generado por Yimi 
        (iniciativas, historias, tareas) y transiciona su estado a READY_FOR_DEV.
        """
        if not os.path.exists(self.state_file):
            return False
            
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                
            updated = False
            for record in state_data.get("backlog_activo", []):
                if record.get("id") == epic_id:
                    record["estado_actual"] = "READY_FOR_DEV"
                    record["desglose"] = breakdown
                    record["fecha_actualizacion"] = datetime.now().isoformat()
                    updated = True
                    break
                    
            if updated:
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump(state_data, f, indent=4, ensure_ascii=False)
                return True
                
            return False
        except Exception:
            return False

    def update_epic_state(self, epic_id: str, new_state: str) -> bool:
        """
        Transiciona el estado de un Epic completo a un nuevo estado (ej. READY_FOR_QA, DONE).
        """
        if not os.path.exists(self.state_file):
            return False
            
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                
            updated = False
            for record in state_data.get("backlog_activo", []):
                if record.get("id") == epic_id:
                    record["estado_actual"] = new_state
                    record["fecha_actualizacion"] = datetime.now().isoformat()
                    updated = True
                    break
                    
            if updated:
                with open(self.state_file, 'w', encoding='utf-8') as f:
                    json.dump(state_data, f, indent=4, ensure_ascii=False)
                return True
                
            return False
        except Exception:
            return False

    def get_epics_by_state(self, target_state: str) -> list:
        """
        Retorna una lista de Epics filtrada por el estado dado.
        """
        if not os.path.exists(self.state_file):
            return []
            
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                
            matches = [record for record in state_data.get("backlog_activo", []) if record.get("estado_actual") == target_state]
            return matches
        except Exception:
            return []
