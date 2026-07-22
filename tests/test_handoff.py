import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.handoff import HandoffManager
from src.core.state_manager import GlobalStateManager

print("--- Inicializando Blackboard para Prueba ---")
# Reset blackboard con un dummy
sm = GlobalStateManager()
epic_id = sm.init_backlog({"dummy": "test"})
sm.update_epic_state(epic_id, "READY_FOR_DEV")

print("\n--- Ejecutando Handoff Manager ---")
hm = HandoffManager()

print("\nCami verifica el backlog...")
pendientes_cami = hm.check_pending_work("cami")
print(f"Cami encontró {len(pendientes_cami)} tareas pendientes.")

if pendientes_cami:
    target_epic = pendientes_cami[0]["id"]
    hm.claim_epic(target_epic, "Cami")
    print("Cami simula que termina el desarrollo y hace handoff a Mani...")
    hm.handoff_to_qa(target_epic, "Cami")

print("\nMani verifica el backlog...")
pendientes_mani = hm.check_pending_work("mani")
print(f"Mani encontró {len(pendientes_mani)} tareas pendientes para QA.")

if pendientes_mani:
    qa_epic = pendientes_mani[0]["id"]
    print("Mani encuentra un error de seguridad y rechaza la tarea...")
    hm.reject_from_qa(qa_epic, "Mani", "Vulnerabilidad XSS en el login")

print("\nCami vuelve a verificar el backlog...")
pendientes_cami2 = hm.check_pending_work("cami")
print(f"Cami encontró {len(pendientes_cami2)} tareas pendientes devueltas o nuevas.")

if pendientes_cami2:
    retry_epic = pendientes_cami2[0]["id"]
    hm.claim_epic(retry_epic, "Cami")
    hm.handoff_to_qa(retry_epic, "Cami")
    
print("\nMani verifica de nuevo y aprueba...")
pendientes_mani2 = hm.check_pending_work("mani")
if pendientes_mani2:
    hm.approve_from_qa(pendientes_mani2[0]["id"], "Mani")

print("\n--- Estado Final del Blackboard ---")
estado_final = sm.get_epics_by_state("DONE")
if estado_final:
    print(f"Exito! EPIC {estado_final[0]['id']} está en estado DONE.")
