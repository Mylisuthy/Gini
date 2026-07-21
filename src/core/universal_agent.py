import os
import json
import subprocess
import google.generativeai as genai

from src.core.memory_manager import memory
from src.core.config_manager import config
from src.skills import yimi_skills

class UniversalAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name.lower().strip()
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
        self.prompt_path = os.path.join(self.prompts_dir, f'{self.agent_name}_prompt.xml')
        
    def _configure_genai(self):
        api_key = config.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada. Ve a la pestaña de Configuración.")
        genai.configure(api_key=api_key)

    def load_prompt(self):
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return f"Eres {self.agent_name.upper()}, Especialista Corporativo."

    def generate_plan(self, user_prompt: str) -> dict:
        try:
            self._configure_genai()
        except Exception as e:
            return {"error": str(e)}

        system_instruction = self.load_prompt()
        
        auto_qa_rule = "\n\nCRÍTICO: Antes de entregar la etiqueta <explicacion> o <archivo>, DEBES generar obligatoriamente la etiqueta <reflexion> criticando tu propia lógica para asegurar máxima calidad corporativa.\nSi necesitas consultar la memoria vectorial, utiliza <buscar_rag>termino</buscar_rag>.\nSi necesitas información de la web, utiliza <buscar_web>termino</buscar_web>.\nSi necesitas probar lógica en Python de forma segura, utiliza <ejecutar_codigo>tu script python</ejecutar_codigo>.\nEl sistema pausará, ejecutará la herramienta y te devolverá el resultado."

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction + auto_qa_rule
        )
        
        context = memory.get_recent_context()
        full_prompt = f"CONTEXTO DE MEMORIA:\n{context}\n\nREQUERIMIENTO ACTUAL:\n{user_prompt}"
        
        try:
            import re
            raw = ""
            
            # Ciclo ReAct (Razonamiento y Acción) - Máximo 3 iteraciones para RAG
            for _ in range(3):
                response = model.generate_content(full_prompt)
                raw = response.text
                
                rag_match = re.search(r'<buscar_rag>(.*?)</buscar_rag>', raw, re.DOTALL)
                web_match = re.search(r'<buscar_web>(.*?)</buscar_web>', raw, re.DOTALL)
                code_match = re.search(r'<ejecutar_codigo>(.*?)</ejecutar_codigo>', raw, re.DOTALL)
                
                if rag_match:
                    termino = rag_match.group(1).strip()
                    rag_results = memory.search_knowledge_base(termino)
                    full_prompt += f"\n\nAsistente (Tú): {raw}\n\nSistema (Resultado RAG): {rag_results}\n\nPor favor, continúa."
                    continue
                elif web_match:
                    from src.skills.secure_tools import ProfessionalWebSearch
                    termino = web_match.group(1).strip()
                    web_results = ProfessionalWebSearch.search(termino)
                    full_prompt += f"\n\nAsistente (Tú): {raw}\n\nSistema (Resultado Web): {web_results}\n\nPor favor, continúa."
                    continue
                elif code_match:
                    from src.skills.secure_tools import SecureExecutionSandbox
                    codigo = code_match.group(1).strip()
                    if codigo.startswith("```"):
                        codigo = codigo.split("\n", 1)[-1]
                    if codigo.endswith("```"):
                        codigo = codigo.rsplit("\n", 1)[0]
                    exec_results = SecureExecutionSandbox.run_python_code(codigo.strip())
                    full_prompt += f"\n\nAsistente (Tú): {raw}\n\nSistema (Salida Sandbox):\n{exec_results}\n\nPor favor, continúa iterando."
                    continue
                else:
                    break
            
            data = {"archivos": [], "comandos": []}
            
            ref_match = re.search(r'<reflexion>(.*?)</reflexion>', raw, re.DOTALL)
            if ref_match:
                data["reflexion"] = ref_match.group(1).strip()
            
            exp_match = re.search(r'<explicacion>(.*?)</explicacion>', raw, re.DOTALL)
            if exp_match:
                data["explicacion"] = exp_match.group(1).strip()
            
            archivos_matches = re.finditer(r'<archivo path="([^"]+)">\s*(.*?)\s*</archivo>', raw, re.DOTALL)
            for m in archivos_matches:
                contenido = m.group(2).strip()
                if contenido.startswith("```"):
                    contenido = contenido.split("\n", 1)[-1]
                if contenido.endswith("```"):
                    contenido = contenido.rsplit("\n", 1)[0]
                data["archivos"].append({"nombre": m.group(1), "contenido": contenido.strip()})
                
            for c_match in re.finditer(r'<comando>(.*?)</comando>', raw, re.DOTALL):
                data["comandos"].append(c_match.group(1).strip())
                
            ev_match = re.search(r'<auto_evolucion>(.*?)</auto_evolucion>', raw, re.DOTALL)
            if ev_match:
                ev_text = ev_match.group(1)
                m = re.search(r'<motivo>(.*?)</motivo>', ev_text, re.DOTALL)
                k = re.search(r'<conocimiento>(.*?)</conocimiento>', ev_text, re.DOTALL)
                if m or k:
                    data["auto_evolucion"] = {
                        "motivo": m.group(1).strip() if m else "",
                        "nuevos_conocimientos": k.group(1).strip() if k else ""
                    }
                    
            az_match = re.search(r'<azure_backlog>(.*?)</azure_backlog>', raw, re.DOTALL)
            if az_match:
                try:
                    import json
                    data["azure_backlog"] = json.loads(az_match.group(1).strip())
                except:
                    pass
                    
            if not data["archivos"] and not data["comandos"] and "explicacion" not in data:
                escaped_raw = raw.replace("<", "&lt;").replace(">", "&gt;")
                data["explicacion"] = "Respuesta parseada: " + escaped_raw
                
            return data
        except Exception as e:
            return {"error": str(e)}

    def execute_plan(self, data: dict, user_prompt: str) -> str:
        log = []
        
        # 1. Crear Archivos Físicos
        archivos = data.get("archivos", [])
        if archivos:
            workspace_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace')
            os.makedirs(workspace_dir, exist_ok=True)
            for file_obj in archivos:
                nombre = file_obj.get("nombre", "unnamed.txt")
                contenido = file_obj.get("contenido", "")
                script_path = os.path.join(workspace_dir, nombre)
                os.makedirs(os.path.dirname(script_path), exist_ok=True)
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(contenido)
                log.append(f"Archivo generado: {nombre}")
        
        # 2. Ejecutar Skills Dinámicas Especializadas
        try:
            import importlib
            skill_module_name = f"src.skills.{self.agent_name}_skills"
            skill_module = importlib.import_module(skill_module_name)
            if hasattr(skill_module, "execute_skills"):
                skill_logs = skill_module.execute_skills(data)
                if skill_logs:
                    log.extend(skill_logs)
        except ImportError:
            pass # El agente no tiene un archivo de skills personalizado
        except Exception as e:
            log.append(f"Error ejecutando skills de {self.agent_name}: {str(e)}")

        # 3. Ejecutar Comandos Terminal
        comandos = data.get("comandos", [])
        if comandos:
            workspace_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace')
            for cmd in comandos:
                log.append(f"Ejecutando: {cmd}")
                try:
                    result = subprocess.run(cmd, shell=True, cwd=workspace_dir, capture_output=True, text=True)
                    if result.stdout:
                        log.append(f"Salida: {result.stdout.strip()}")
                    if result.stderr:
                        log.append(f"Error STDERR: {result.stderr.strip()}")
                except Exception as e:
                    log.append(f"Error lanzando comando: {str(e)}")

        # 4. Procesar Auto-Evolución Autónoma (Evo en Segundo Plano)
        auto_ev = data.get("auto_evolucion")
        if auto_ev:
            try:
                motivo = auto_ev.get("motivo", "")
                conocimiento = auto_ev.get("nuevos_conocimientos", "")
                if conocimiento:
                    from src.core.evo_agent import EvoAgent
                    evo = EvoAgent()
                    evo_request = f"El agente '{self.agent_name}' intentó hacer una tarea pero falló o requiere mejorar. Motivo: {motivo}. \nConocimiento sugerido para integrar permanentemente: {conocimiento}.\nPor favor, reescribe la matriz completa de {self.agent_name} agregando esta regla. Usa la etiqueta <archivo path='...'>."
                    
                    evo_decision = evo.analyze_request(evo_request)
                    if evo_decision.get("action") == "update_agent":
                        new_xml = evo_decision.get("prompt_content")
                        if new_xml:
                            result_msg = evo.execute_update(self.agent_name, new_xml)
                            log.append(f"🧬 [EVO AUTÓNOMO] {result_msg}")
                    else:
                        log.append(f"🧬 [EVO AUTÓNOMO] Evo analizó el caso pero decidió no modificar al agente.")
            except Exception as e:
                log.append(f"❌ Fallo al intentar auto-evolucionar con Evo: {str(e)}")

        msg_success = "\n".join(log) if log else "Plan ejecutado (sin acciones físicas)."
        memory.save_interaction(self.agent_name.capitalize(), "Especialista", user_prompt, msg_success)
        return msg_success
