import os
import threading
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List

from src.core.router import GiniRouter
from src.core.universal_agent import UniversalAgent
from src.core.config_manager import config

app = FastAPI(title="Gini V8.0 Zero-Node API")

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    text: str

class AgentGenerateRequest(BaseModel):
    agent_name: str
    prompt: str

class AgentExecuteRequest(BaseModel):
    agent_name: str
    plan_data: Dict[str, Any]

class SettingsRequest(BaseModel):
    gemini_api_key: str
    tavily_api_key: str
    azure_pat: str = ""
    azure_org: str = ""
    azure_project: str = ""

@app.post("/api/chat")
async def chat_route(req: ChatRequest):
    try:
        router = GiniRouter()
        intent = router.analyze_intent(req.text)
        
        if intent["action"] == "route_multiple":
            plan = {}
            for target in intent["targets"]:
                plan[target["agent"]] = target["message"]
            return {"success": True, "plan": plan, "is_direct_response": False}
        else:
            return {"success": True, "direct_response": intent["message"], "is_direct_response": True}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.post("/api/agent/generate")
async def agent_generate(req: AgentGenerateRequest):
    try:
        agent = UniversalAgent(agent_name=req.agent_name.lower())
        if not agent:
            return JSONResponse(status_code=404, content={"success": False, "error": f"Agent {req.agent_name} not found"})
        
        plan_data = agent.generate_plan(req.prompt)
        return {"success": True, "plan_data": plan_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.post("/api/agent/execute")
async def agent_execute(req: AgentExecuteRequest):
    try:
        agent = UniversalAgent(agent_name=req.agent_name.lower())
        if not agent:
            return JSONResponse(status_code=404, content={"success": False, "error": f"Agent {req.agent_name} not found"})
        
        # Guardar en memoria si es necesario
        from src.core.memory_manager import memory
        memory.save_interaction("user", f"Approve execution for {req.agent_name}")
        
        results = agent.execute_plan(req.plan_data)
        return {"success": True, "results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.post("/api/settings")
async def save_settings(req: SettingsRequest):
    try:
        if req.gemini_api_key:
            config.set("GEMINI_API_KEY", req.gemini_api_key)
        if req.tavily_api_key:
            config.set("TAVILY_API_KEY", req.tavily_api_key)
        if req.azure_pat:
            config.set("AZURE_DEVOPS_PAT", req.azure_pat)
        if req.azure_org:
            config.set("AZURE_DEVOPS_ORG", req.azure_org)
        if req.azure_project:
            config.set("AZURE_DEVOPS_PROJECT", req.azure_project)
            
        return {"success": True, "message": "Configuración segura guardada exitosamente"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

# Montar frontend estático
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

