import os
import google.generativeai as genai
from src.core.config_manager import config

class SwarmFactory:
    def __init__(self):
        api_key = config.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada.")
        genai.configure(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
    def execute_swarm(self, micro_agents_list: list, base_context: str) -> str:
        """
        Ejecuta una cadena de micro-agentes de forma secuencial.
        micro_agents_list: [{"rol": "Micro-Arquitecto", "tarea": "..."}]
        """
        swarm_log = []
        current_context = base_context
        
        for agent_def in micro_agents_list:
            rol = agent_def.get("rol", "Micro-Agente")
            tarea = agent_def.get("tarea", "")
            
            system_prompt = f"Eres un {rol} altamente especializado. Eres parte de un micro-enjambre efímero y reportas directamente al Líder Técnico. No tienes interfaz con el usuario final. Tu única responsabilidad es ejecutar esta tarea de forma perfecta y devolver el resultado técnico en bruto (código, arquitectura, test, etc.)."
            
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_prompt
                )
                
                full_prompt = f"CONTEXTO GENERAL Y RESULTADOS ANTERIORES:\n{current_context}\n\nTU TAREA ESPECÍFICA:\n{tarea}"
                response = model.generate_content(full_prompt)
                resultado = response.text
                
                current_context += f"\n\n--- Resultado de {rol} ---\n{resultado}"
                swarm_log.append(f"[{rol}] completó su tarea.")
                
            except Exception as e:
                swarm_log.append(f"[{rol}] falló: {str(e)}")
                current_context += f"\n\n--- Falla de {rol} ---\nError: {str(e)}"
                
        # Retornamos el contexto acumulado que contiene todo el trabajo realizado
        return current_context
