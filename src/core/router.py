import sys
import os

# Parche crítico para resolver el módulo 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

from src.core.memory_manager import memory
from src.core.state_manager import GlobalStateManager

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GiniRouter:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash"
        )
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        self.prompt_path = os.path.join(self.prompts_dir, 'gini_prompt.xml')

    def get_system_prompt(self):
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return "Eres GINI, Enrutadora de Sistemas. Retorna JSON."

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
                targets = []
                for m in enrutar_matches:
                    target_agent = m.group(1).lower()
                    raw_message = m.group(2).strip()
                    
                    if target_agent == 'yimi':
                        # Formatear y registrar estado
                        try:
                            # Buscar posible contenido JSON (limpiar posibles codeblocks ```json)
                            clean_message = raw_message.replace("```json\n", "").replace("```", "").strip()
                            payload = json.loads(clean_message)
                            state_manager = GlobalStateManager()
                            epic_id = state_manager.init_backlog(payload)
                            
                            payload["epic_id"] = epic_id
                            targets.append({"agent": target_agent, "message": json.dumps(payload, indent=2, ensure_ascii=False)})
                        except Exception:
                            # Fallback
                            state_manager = GlobalStateManager()
                            epic_id = state_manager.init_backlog({"raw_text": raw_message})
                            targets.append({"agent": target_agent, "message": raw_message})
                    else:
                        # Este caso en teoría no debería ocurrir dado el nuevo prompt
                        targets.append({"agent": target_agent, "message": raw_message})
                        
                return {"action": "route_multiple", "targets": targets}
                
            responder_match = re.search(r'<responder>(.*?)</responder>', raw, re.DOTALL)
            if responder_match:
                msg_match = re.search(r'<mensaje>(.*?)</mensaje>', responder_match.group(1), re.DOTALL)
                msg = msg_match.group(1).strip() if msg_match else responder_match.group(1).strip()
                return {"action": "respond", "message": msg}
                
            return {"action": "respond", "message": "Respuesta no estandarizada: " + raw}
        except Exception as e:
            return {"action": "respond", "message": f"Error interno en el sistema de enrutamiento: {str(e)}"}
