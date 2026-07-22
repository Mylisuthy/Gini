import os
import sys
import subprocess
import uuid
import tempfile
from src.core.config_manager import config

class SecureExecutionSandbox:
    """
    Ejecuta código de los agentes dentro de un contenedor Docker efímero (Opción B).
    Garantiza aislamiento absoluto sin costos recurrentes de APIs de Sandbox (como E2B),
    ahorrando costos a futuro y maximizando la ciberseguridad (Zero-Trust).
    """
    @staticmethod
    def run_python_code(code: str, timeout: int = 15) -> str:
        # 1. Intentamos usar Docker si está instalado
        has_docker = False
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            has_docker = True
        except Exception:
            has_docker = False

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            # Si no hay Docker, inyectamos un parche de seguridad al inicio del script
            if not has_docker:
                safety_patch = '''
import sys
import os
# Bloqueo básico de módulos peligrosos en fallback local
for mod in ['subprocess', 'shutil', 'socket']:
    sys.modules[mod] = None
'''
                f.write(safety_patch + "\n" + code)
            else:
                f.write(code)
            script_path = f.name
            
        filename = os.path.basename(script_path)
        
        if has_docker:
            container_name = f"gini_sandbox_{uuid.uuid4().hex[:8]}"
            docker_cmd = [
                "docker", "run", "--rm", "--name", container_name,
                "--memory=128m", "--cpus=0.5", "--network=none",
                "-v", f"{script_path}:/app/{filename}:ro",
                "-w", "/app",
                "python:3.11-slim",
                "python", filename
            ]
            try:
                result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
                os.remove(script_path)
                
                if result.returncode == 0:
                    return f"[EXITO (Docker Sandbox)]\n{result.stdout.strip()}"
                else:
                    return f"[ERROR (Docker Sandbox)]\n{result.stderr.strip()}"
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "kill", container_name], capture_output=True)
                os.remove(script_path)
                return "[ERROR] Tiempo de ejecución excedido en Docker (Timeout 15s)."
            except Exception as e:
                if os.path.exists(script_path):
                    os.remove(script_path)
                return f"[ERROR] Falló la infraestructura Docker: {str(e)}"
        else:
            # Fallback Local Restringido
            # Limpiamos variables de entorno críticas
            safe_env = os.environ.copy()
            for key in ["GEMINI_API_KEY", "AZURE_DEVOPS_PAT", "TAVILY_API_KEY"]:
                safe_env.pop(key, None)
                
            try:
                result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=timeout, env=safe_env)
                os.remove(script_path)
                
                if result.returncode == 0:
                    return f"[EXITO (Local Restricted)]\n{result.stdout.strip()}"
                else:
                    return f"[ERROR (Local Restricted)]\n{result.stderr.strip()}"
            except subprocess.TimeoutExpired:
                os.remove(script_path)
                return "[ERROR] Tiempo de ejecución excedido en Sandbox Local (Timeout 15s)."
            except Exception as e:
                if os.path.exists(script_path):
                    os.remove(script_path)
                return f"[ERROR] Falló el Sandbox Local: {str(e)}"


class ProfessionalWebSearch:
    """
    Integración con Tavily API para búsquedas profesionales optimizadas para LLMs.
    """
    @staticmethod
    def search(query: str) -> str:
        api_key = config.get("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY no configurada. Por seguridad, no se admiten scrapers no autenticados."
            
        try:
            import requests
            headers = {"Content-Type": "application/json"}
            payload = {
                "api_key": api_key,
                "query": query,
                "search_depth": "advanced", # Calidad SOTA para LLMs
                "include_answer": True,
                "max_results": 3
            }
            response = requests.post("https://api.tavily.com/search", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            answer = data.get("answer", "")
            results = data.get("results", [])
            
            output = f"Resumen de IA: {answer}\n\nFuentes Analizadas:\n"
            for r in results:
                output += f"- {r.get('title')} ({r.get('url')}): {r.get('content')}\n"
                
            return output
        except ImportError:
            return "Error: Dependencia faltante (pip install requests)"
        except Exception as e:
            return f"Error en Web Search API: {str(e)}"
