import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.skills.secure_tools import SecureExecutionSandbox

print("--- Test: Script Seguro ---")
safe_code = """
print("Hola Mundo desde Sandbox")
"""
res_safe = SecureExecutionSandbox.run_python_code(safe_code)
print(res_safe)

print("\n--- Test: Intento de leer variables de entorno ---")
env_code = """
import os
print("API Key:", os.environ.get("GEMINI_API_KEY", "No Encontrada"))
"""
res_env = SecureExecutionSandbox.run_python_code(env_code)
print(res_env)

print("\n--- Test: Intento de usar subprocess ---")
sub_code = """
import subprocess
print(subprocess.check_output('echo hack', shell=True))
"""
res_sub = SecureExecutionSandbox.run_python_code(sub_code)
print(res_sub)
