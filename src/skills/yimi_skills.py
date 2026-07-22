# Yimi Skills
# Herramientas exclusivas del Planeador (Product Owner y Experto Azure DevOps)

import json
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from src.core.state_manager import GlobalStateManager

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv()

# Credenciales y Configuración de Azure
ORGANIZATION = os.getenv("AZURE_ORGANIZATION")
PROJECT = os.getenv("AZURE_PROJECT")
PAT = os.getenv("AZURE_DEVOPS_PAT")

if ORGANIZATION and PROJECT:
    BASE_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems"
else:
    BASE_URL = ""

HEADERS = {'Content-Type': 'application/json-patch+json'}

# --- Integración con Azure DevOps ---

def _add_parent_link(payload: list, parent_id: int):
    if parent_id and parent_id > 0 and BASE_URL:
        org_proj_url = BASE_URL.replace("/_apis/wit/workitems", "")
        parent_url = f"{org_proj_url}/_apis/wit/workItems/{parent_id}"
        payload.append({
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": parent_url
            }
        })

def _enviar_peticion_azure(tipo_item: str, payload_patch: list) -> tuple:
    """Función base segura para ejecutar POST a la API REST de Azure. Retorna (item_id, mensaje)."""
    if not PAT or not BASE_URL:
        return (-1, "Error: Faltan credenciales de Azure en el archivo .env")
        
    url = f"{BASE_URL}/${tipo_item}?api-version=7.0"
    response = requests.post(url, json=payload_patch, headers=HEADERS, auth=HTTPBasicAuth('', PAT))
    
    if response.status_code in [200, 201]:
        data = response.json()
        item_id = data.get('id')
        return (item_id, f"Éxito: {tipo_item} creado en Azure con ID {item_id}.")
    else:
        return (-1, f"Error {response.status_code}: {response.text}")

def crear_iniciativa(titulo: str, descripcion: str, fecha_inicio: str, fecha_objetivo: str, tipo_iniciativa: str, prioridad: str) -> tuple:
    """Crea una Iniciativa en Azure DevOps siguiendo reglas de Celsia."""
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": titulo},
        {"op": "add", "path": "/fields/System.Description", "value": descripcion},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StartDate", "value": fecha_inicio},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.TargetDate", "value": fecha_objetivo},
        {"op": "add", "path": "/fields/Custom.InitiativeType", "value": tipo_iniciativa},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": prioridad}
    ]
    return _enviar_peticion_azure("Iniciativa", payload)

def crear_historia_usuario(titulo: str, descripcion: str, story_points: int, parent_id: int = None) -> tuple:
    """Crea un User Story en Azure DevOps con puntos de historia. Vincula al padre si se provee parent_id."""
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": titulo},
        {"op": "add", "path": "/fields/System.Description", "value": descripcion},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": story_points}
    ]
    _add_parent_link(payload, parent_id)
    return _enviar_peticion_azure("User Story", payload)

def registrar_bug(titulo: str, pasos_reproduccion: str, severidad: str, stage: str, story_points: int, parent_id: int = None) -> tuple:
    """Registra un Bug en Azure DevOps con el campo Found In Stage."""
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": titulo},
        {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ReproSteps", "value": pasos_reproduccion},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Severity", "value": severidad},
        {"op": "add", "path": "/fields/Custom.FoundInStage", "value": stage},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": story_points}
    ]
    _add_parent_link(payload, parent_id)
    return _enviar_peticion_azure("Bug", payload)

def crear_tarea(titulo: str, descripcion: str, actividad: str, horas_estimadas: float, parent_id: int = None) -> tuple:
    """Crea una Task técnica en Azure asegurando la regla de actividad y horas. Vincula al padre si se provee parent_id."""
    if horas_estimadas > 16:
        return (-1, "Rechazado: La estimación supera el límite máximo por excepción de 16 horas. Solicite justificación al usuario.")
        
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": titulo},
        {"op": "add", "path": "/fields/System.Description", "value": descripcion},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Activity", "value": actividad},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate", "value": horas_estimadas}
    ]
    _add_parent_link(payload, parent_id)
    return _enviar_peticion_azure("Task", payload)

def execute_skills(data: dict) -> list:
    log = []
    azure_backlog = data.get("azure_backlog")
    
    if not azure_backlog:
        return log
        
    epic_id = azure_backlog.get("epic_id")
    
    # 1. Registrar en el Blackboard (Local State Manager)
    if epic_id:
        try:
            state_manager = GlobalStateManager()
            success = state_manager.update_epic_with_breakdown(epic_id, azure_backlog)
            if success:
                log.append(f"Blackboard actualizado: Epic {epic_id} transicionado a READY_FOR_DEV con su desglose.")
            else:
                log.append(f"Aviso: No se pudo actualizar el Epic {epic_id} en el Blackboard (no encontrado o corrupto).")
        except Exception as e:
            log.append(f"Error interno al escribir en el Blackboard: {str(e)}")

    # 2. Modo Espejo: Registrar en Azure DevOps
    if "iniciativa" in azure_backlog:
        try:
            ini = azure_backlog["iniciativa"]
            ini_id, res_ini = crear_iniciativa(
                titulo=ini.get("titulo"), descripcion=ini.get("descripcion"),
                fecha_inicio=ini.get("fecha_inicio"), fecha_objetivo=ini.get("fecha_objetivo"),
                tipo_iniciativa=ini.get("tipo_iniciativa"), prioridad=str(ini.get("prioridad"))
            )
            log.append(f"Iniciativa Azure: {res_ini}")
            
            for story in azure_backlog.get("historias", []):
                story_id, res_story = crear_historia_usuario(
                    titulo=story.get("titulo"), descripcion=story.get("descripcion"),
                    story_points=story.get("story_points"), parent_id=ini_id if ini_id > 0 else None
                )
                log.append(f"Story Azure: {res_story}")
                
                for task in story.get("tareas", []):
                    task_id, res_task = crear_tarea(
                        titulo=task.get("titulo"), descripcion=task.get("descripcion"),
                        actividad=task.get("actividad"), horas_estimadas=float(task.get("horas_estimadas", 1)),
                        parent_id=story_id if story_id > 0 else None
                    )
                    log.append(f"Tarea Azure: {res_task}")
        except Exception as e:
            log.append(f"Error en Azure DevOps: {str(e)}")
    return log
