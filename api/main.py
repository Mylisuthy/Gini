from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import sys
import os
import threading

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.core.router import GiniRouter
from src.core.universal_agent import UniversalAgent
from src.core.state_manager import GlobalStateManager

app = FastAPI(title="Gini Zero-Node API")

# Serve UI files
ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui")
os.makedirs(ui_path, exist_ok=True)

class ChatRequest(BaseModel):
    message: str

class AgentProcessThread(threading.Thread):
    def __init__(self, targets):
        super().__init__()
        self.targets = targets

    def run(self):
        for target in self.targets:
            agent_name = target.get("agent")
            message = target.get("message")
            if agent_name:
                print(f"--- Iniciando procesamiento asíncrono para {agent_name} ---")
                agent = UniversalAgent(agent_name)
                # Aquí normalmente generaríamos el plan y lo ejecutaríamos.
                # Como es asíncrono, los resultados se escriben al Blackboard.
                plan = agent.generate_plan(message)
                if "error" not in plan:
                    agent.execute_plan(plan, message)

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    router = GiniRouter()
    result = router.analyze_intent(req.message)
    
    if result.get("action") == "route_multiple":
        # Disparamos los agentes en un hilo en background para no bloquear la UI
        thread = AgentProcessThread(result.get("targets", []))
        thread.start()
        
        return JSONResponse({"status": "routed", "message": "Tu requerimiento ha sido empaquetado y enviado a los líderes. Revisa el Blackboard para ver el progreso."})
    else:
        return JSONResponse({"status": "responded", "message": result.get("message", "Sin respuesta.")})

@app.get("/api/blackboard")
async def get_blackboard():
    sm = GlobalStateManager()
    state_file = sm.state_file
    if os.path.exists(state_file):
        import json
        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JSONResponse(data)
    return JSONResponse({"backlog_activo": [], "historico": []})

app.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")
