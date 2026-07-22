import json
from src.core.state_manager import GlobalStateManager

class HandoffManager:
    """
    Gestiona las transferencias laterales (Peer-to-Peer) entre los Líderes Técnicos
    y el Blackboard, eliminando la dependencia de Gini como orquestador central.
    """
    def __init__(self):
        self.state_manager = GlobalStateManager()

    def claim_epic(self, epic_id: str, leader_name: str) -> bool:
        """
        Un líder reclama un Epic que estaba en READY_FOR_DEV, pasándolo a IN_PROGRESS.
        """
        success = self.state_manager.update_epic_state(epic_id, "IN_PROGRESS")
        if success:
            print(f"[{leader_name.upper()}] ha reclamado el EPIC {epic_id}. Estado -> IN_PROGRESS")
        return success

    def handoff_to_qa(self, epic_id: str, leader_name: str) -> bool:
        """
        El líder de Dev finaliza y transfiere el Epic a QA.
        """
        success = self.state_manager.update_epic_state(epic_id, "READY_FOR_QA")
        if success:
            print(f"[{leader_name.upper()}] ha finalizado el desarrollo del EPIC {epic_id}. Estado -> READY_FOR_QA")
        return success

    def reject_from_qa(self, epic_id: str, qa_name: str, reason: str) -> bool:
        """
        QA rechaza el Epic y lo devuelve a IN_PROGRESS.
        """
        success = self.state_manager.update_epic_state(epic_id, "REJECTED_BY_QA")
        if success:
            print(f"[{qa_name.upper()}] ha RECHAZADO el EPIC {epic_id} por: {reason}. Estado -> REJECTED_BY_QA")
        return success

    def approve_from_qa(self, epic_id: str, qa_name: str) -> bool:
        """
        QA aprueba el Epic y lo marca como DONE.
        """
        success = self.state_manager.update_epic_state(epic_id, "DONE")
        if success:
            print(f"[{qa_name.upper()}] ha APROBADO el EPIC {epic_id}. Estado -> DONE")
        return success

    def check_pending_work(self, leader_role: str) -> list:
        """
        Un líder consulta el Blackboard para saber si hay trabajo pendiente para su rol.
        - Dev Leaders (Cami/Fani) buscan READY_FOR_DEV o REJECTED_BY_QA.
        - QA Leaders (Mani) buscan READY_FOR_QA.
        """
        pending = []
        if leader_role.lower() in ['cami', 'fani', 'dev']:
            pending.extend(self.state_manager.get_epics_by_state("READY_FOR_DEV"))
            pending.extend(self.state_manager.get_epics_by_state("REJECTED_BY_QA"))
        elif leader_role.lower() in ['mani', 'qa', 'tester']:
            pending.extend(self.state_manager.get_epics_by_state("READY_FOR_QA"))
            
        return pending
