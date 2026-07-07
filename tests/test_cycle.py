import sys
import os
import time

# Agregar src al path para importar
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.router import GiniRouter
from src.core.handoff import HandoffProtocol

def simular_ciclo_completo():
    print("🚀 INICIANDO SIMULACIÓN DE ECOSISTEMA: Gini -> Yimi -> Cami -> Fani -> Mani\n")
    
    # --- 1. GINI (Orquestadora) ---
    router = GiniRouter()
    user_prompt = "Necesito un sistema de login seguro con validación en base de datos y una interfaz web agradable."
    
    print("🌸 [Gini]: Recibiendo petición del usuario...")
    route_info = router.route_task(user_prompt) # Gini decide a quién mandar (Debería ser a Yimi para planear)
    
    # Forzamos flujo lineal para la simulación
    handoff_pkg = HandoffProtocol.create_initial_package("Gini", "Yimi", user_prompt)
    print("📦 [Protocolo] Paquete Inicial Creado.")
    time.sleep(1)
    
    # --- 2. YIMI (Planeador) ---
    print("\n📝 [Yimi]: Analizando la petición... Generando User Stories y Criterios de Aceptación.")
    yimi_deliverable = {
        "epic": "Sistema de Autenticación",
        "user_stories": ["Como usuario quiero hacer login para ver mi perfil."],
        "acceptance_criteria": ["La contraseña debe estar encriptada", "La UI debe tener feedback visual de error"]
    }
    handoff_pkg = HandoffProtocol.pass_baton(
        handoff_pkg, "Yimi", "Cami", "yimi_plan", yimi_deliverable, "Plan creado, pasando a Backend"
    )
    time.sleep(1)
    
    # --- 3. CAMI (Backend) ---
    print("\n⚙️ [Cami]: Leyendo el plan de Yimi... Construyendo API y esquema de DB.")
    cami_deliverable = {
        "db_schema": {"users": {"id": "uuid", "email": "varchar", "password_hash": "varchar"}},
        "api_endpoints": ["POST /api/login"]
    }
    handoff_pkg = HandoffProtocol.pass_baton(
        handoff_pkg, "Cami", "Fani", "cami_backend", cami_deliverable, "API y DB listas. Pasando a Frontend."
    )
    time.sleep(1)

    # --- 4. FANI (Frontend) ---
    print("\n🎨 [Fani]: Consumiendo la API de Cami... Diseñando interfaz en React.")
    fani_deliverable = {
        "components": ["LoginForm.jsx", "AuthButton.css"],
        "ui_state": "Redux Auth Slice"
    }
    handoff_pkg = HandoffProtocol.pass_baton(
        handoff_pkg, "Fani", "Mani", "fani_frontend", fani_deliverable, "UI maquetada y conectada. Pasando a QA."
    )
    time.sleep(1)

    # --- 5. MANI (QA & Tester) ---
    print("\n🛡️ [Mani]: Recibiendo build... Auditando contra Criterios de Aceptación de Yimi.")
    mani_deliverable = {
        "status": "APPROVED",
        "tests_passed": 12,
        "tests_failed": 0,
        "notes": "Encriptación validada. Feedback visual correcto."
    }
    handoff_pkg = HandoffProtocol.pass_baton(
        handoff_pkg, "Mani", "Done", "mani_qa_report", mani_deliverable, "Todas las pruebas en verde. Listo para producción."
    )
    time.sleep(1)

    print("\n✅ CICLO COMPLETADO. ESTADO FINAL DEL PAQUETE:")
    print(HandoffProtocol.render_package(handoff_pkg))

if __name__ == "__main__":
    # Ajuste para evitar problemas con emojis en consola Windows
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    simular_ciclo_completo()
