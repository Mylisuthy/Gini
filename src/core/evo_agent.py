import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from src.core.memory_manager import memory

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class EvoAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash"
        )
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        self.prompt_path = os.path.join(self.prompts_dir, 'evo_prompt.xml')

    def get_all_agents_config(self) -> str:
        """Lee todos los archivos de prompts para que Evo sepa cómo están configurados."""
        configs = []
        if os.path.exists(self.prompts_dir):
            for filename in os.listdir(self.prompts_dir):
                if filename.endswith("_prompt.xml") and filename != "evo_prompt.xml":
                    agent_name = filename.replace("_prompt.xml", "")
                    try:
                        with open(os.path.join(self.prompts_dir, filename), 'r', encoding='utf-8') as f:
                            content = f.read()
                            configs.append(f"--- AGENTE: {agent_name.upper()} ---\n{content}\n")
                    except Exception:
                        pass
        return "\n".join(configs)

    def analyze_request(self, user_prompt: str) -> dict:
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
        except Exception:
            system_prompt = "Eres EVO, Arquitecto de Agentes. Retorna XML."
            
        current_configs = self.get_all_agents_config()
        full_system = system_prompt + f"\n\nCONFIGURACIÓN ACTUAL DEL ENJAMBRE:\n{current_configs}"
        
        context = memory.get_recent_context()
        full_prompt = f"CONTEXTO RECIENTE:\n{context}\n\nNUEVO REQUERIMIENTO DEL ADMINISTRADOR:\n{user_prompt}"
        
        try:
            response = self.model.generate_content(full_system + "\n\n" + full_prompt)
            raw = response.text
            import re
            
            resp_match = re.search(r'<responder>(.*?)</responder>', raw, re.DOTALL)
            if resp_match:
                msg_match = re.search(r'<mensaje>(.*?)</mensaje>', resp_match.group(1), re.DOTALL)
                msg = msg_match.group(1).strip() if msg_match else resp_match.group(1).strip()
                return {"action": "respond", "message": msg}
                
            archivo_match = re.search(r'<archivo path="([^"]+)">\s*(.*?)\s*</archivo>', raw, re.DOTALL)
            if archivo_match:
                path = archivo_match.group(1)
                content = archivo_match.group(2)
                agent_name = os.path.basename(path).replace("_prompt.xml", "")
                return {"action": "update_agent", "agent_name": agent_name, "prompt_content": content}
                
            comando_match = re.search(r'<comando>(.*?)</comando>', raw, re.DOTALL)
            if comando_match:
                cmd = comando_match.group(1)
                if "del " in cmd or "rm " in cmd:
                    name_match = re.search(r'([a-zA-Z0-9_]+)_prompt\.xml', cmd)
                    if name_match:
                        return {"action": "delete_agent", "agent_name": name_match.group(1)}
                        
            sim_match = re.search(r'<simular target="([^"]+)">(.*?)</simular>', raw, re.DOTALL)
            if sim_match:
                return {"action": "test_agent", "agent_name": sim_match.group(1), "prompt_test": sim_match.group(2).strip()}
                
            return {"action": "respond", "message": "Respuesta Evo parseada: " + raw}
        except Exception as e:
            return {"action": "respond", "message": f"Error interno en EVO: {str(e)}"}

    def execute_update(self, agent_name: str, new_prompt_content: str) -> str:
        """Guarda físicamente el nuevo prompt en el disco, evolucionando al agente."""
        safe_name = agent_name.lower().strip()
        filepath = os.path.join(self.prompts_dir, f"{safe_name}_prompt.xml")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_prompt_content)
            
            memory.save_interaction("Evo", "Arquitecto", f"Modificar agente {safe_name}", f"Se actualizó la matriz de personalidad de {safe_name}.")
            return f"Agente '{safe_name}' ha sido configurado y guardado en disco exitosamente. Gini ya está al tanto de sus nuevas capacidades."
        except Exception as e:
            return f"Error al guardar configuración: {str(e)}"

    def execute_delete(self, agent_name: str) -> str:
        safe_name = agent_name.lower().strip()
        if safe_name in ["gini", "evo"]:
            return "No puedes eliminar a los agentes core (Gini o Evo)."
            
        filepath = os.path.join(self.prompts_dir, f"{safe_name}_prompt.xml")
        if os.path.exists(filepath):
            os.remove(filepath)
            memory.save_interaction("Evo", "Arquitecto", f"Eliminar agente {safe_name}", f"El agente {safe_name} fue purgado del ecosistema.")
            return f"El agente '{safe_name}' ha sido eliminado exitosamente. Gini ya no le asignará tareas."
        return f"El agente '{safe_name}' no existe."
