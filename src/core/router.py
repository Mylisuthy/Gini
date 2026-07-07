import sys
import os

# Parche crítico para resolver el módulo 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

from src.core.memory_manager import memory

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GiniRouter:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash"
        )
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        self.prompt_path = os.path.join(self.prompts_dir, 'gini_prompt.xml')

    def get_dynamic_agents_list(self) -> str:
        """Escanea dinámicamente los agentes disponibles y sus roles desde archivos XML."""
        import re
        agents_info = []
        if os.path.exists(self.prompts_dir):
            for filename in os.listdir(self.prompts_dir):
                if filename.endswith("_prompt.xml") and filename not in ["gini_prompt.xml", "evo_prompt.xml"]:
                    try:
                        with open(os.path.join(self.prompts_dir, filename), 'r', encoding='utf-8') as f:
                            content = f.read()
                            id_match = re.search(r'<id>(.*?)</id>', content)
                            role_match = re.search(r'<role>(.*?)</role>', content)
                            if id_match and role_match:
                                agents_info.append(f'- "{id_match.group(1)}": {role_match.group(1)}')
                    except Exception:
                        pass
        return "\n".join(agents_info)

    def get_system_prompt(self):
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                base_prompt = f.read()
        except Exception:
            base_prompt = "Eres GINI, Enrutadora de Sistemas. Retorna JSON."
            
        dynamic_list = self.get_dynamic_agents_list()
        
        # Inyectar lista dinámica en el prompt base de Gini
        full_system_prompt = base_prompt + f"\n\nEspecialistas disponibles (generado dinámicamente):\n{dynamic_list}"
        return full_system_prompt

    def analyze_intent(self, user_prompt: str) -> Dict[str, Any]:
        context = memory.get_recent_context()
        system_prompt = self.get_system_prompt()
        full_prompt = f"CONTEXTO RECIENTE:\n{context}\n\nNUEVO MENSAJE DEL USUARIO:\n{user_prompt}"
        
        try:
            response = self.model.generate_content(
                system_prompt + "\n\n" + full_prompt
            )
            raw = response.text
            import re
            
            enrutar_matches = list(re.finditer(r'<enrutar target="([^"]+)">(.*?)</enrutar>', raw, re.DOTALL))
            if enrutar_matches:
                targets = [{"agent": m.group(1).lower(), "message": m.group(2).strip()} for m in enrutar_matches]
                return {"action": "route_multiple", "targets": targets}
                
            responder_match = re.search(r'<responder>(.*?)</responder>', raw, re.DOTALL)
            if responder_match:
                msg_match = re.search(r'<mensaje>(.*?)</mensaje>', responder_match.group(1), re.DOTALL)
                msg = msg_match.group(1).strip() if msg_match else responder_match.group(1).strip()
                return {"action": "respond", "message": msg}
                
            auto_ev_match = re.search(r'<auto_evolucion>(.*?)</auto_evolucion>', raw, re.DOTALL)
            if auto_ev_match:
                ev_text = auto_ev_match.group(1)
                mot_match = re.search(r'<motivo>(.*?)</motivo>', ev_text, re.DOTALL)
                con_match = re.search(r'<conocimiento>(.*?)</conocimiento>', ev_text, re.DOTALL)
                motivo = mot_match.group(1).strip() if mot_match else "Necesidad detectada."
                conoc = con_match.group(1).strip() if con_match else "Recomiendo llamar a Evo."
                return {"action": "respond", "message": f"🤖 **Alerta de Auto-Evolución**\n\nHe detectado un vacío en nuestro equipo:\n- **Motivo:** {motivo}\n- **Acción Sugerida:** {conoc}\n\n¿Quieres que llame a EVO para crear este agente?"}
                
            return {"action": "respond", "message": "Respuesta no estandarizada: " + raw}
        except Exception as e:
            return {"action": "respond", "message": f"Error interno en el sistema de enrutamiento: {str(e)}"}
