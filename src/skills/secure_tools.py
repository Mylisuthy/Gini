import os
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
        # Verificamos si Docker está instalado
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except Exception:
            return "Error: Docker no está instalado o en ejecución. El Sandbox de seguridad corporativa lo requiere estrictamente."

        # Creamos un archivo temporal para el script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            script_path = f.name
            
        filename = os.path.basename(script_path)
        container_name = f"gini_sandbox_{uuid.uuid4().hex[:8]}"
        
        # Ejecutamos el contenedor efímero aislando red y recursos
        docker_cmd = [
            "docker", "run", "--rm", "--name", container_name,
            "--memory=128m", "--cpus=0.5", "--network=none", # Seguridad máxima: sin red
            "-v", f"{script_path}:/app/{filename}:ro", # Solo lectura
            "-w", "/app",
            "python:3.11-slim",
            "python", filename
        ]
        
        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
            os.remove(script_path)
            
            if result.returncode == 0:
                return f"[EXITO]\n{result.stdout.strip()}"
            else:
                return f"[ERROR]\n{result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", container_name], capture_output=True)
            os.remove(script_path)
            return "[ERROR] Tiempo de ejecución excedido (Timeout de seguridad de 15s)."
        except Exception as e:
            if os.path.exists(script_path):
                os.remove(script_path)
            return f"[ERROR] Falló la infraestructura del Sandbox: {str(e)}"


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
