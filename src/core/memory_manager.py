import os
from datetime import datetime

class MemoryManager:
    def __init__(self):
        # La carpeta de memoria estará al nivel de src
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'memory')
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
            
    def _get_today_filepath(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(self.memory_dir, f"{today_str}.md")

    def save_interaction(self, agent_name: str, role: str, user_prompt: str, agent_response: str):
        filepath = self._get_today_filepath()
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Formato limpio y enlazable en markdown
        entry = f"## [{timestamp}] Interacción con {agent_name} ({role})\n"
        if user_prompt:
            entry += f"**Usuario:**\n> {user_prompt.strip()}\n\n"
        if agent_response:
            entry += f"**{agent_name}:**\n{agent_response.strip()}\n\n"
        entry += "---\n\n"
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(entry)

    def get_recent_context(self, max_chars=30000) -> str:
        """Devuelve el contexto de hoy ultra-comprimido."""
        filepath = self._get_today_filepath()
        if not os.path.exists(filepath):
            return "No hay contexto previo para hoy."
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Retornar los últimos N caracteres para no desbordar el contexto del LLM
        if len(content) > max_chars:
            return "... [Contenido truncado] ...\n" + content[-max_chars:]
        return content

# Instancia global
memory = MemoryManager()
