import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.router import GiniRouter

def test_gini_router_multiple_routing():
    """Prueba que el router extrae correctamente multiples etiquetas XML de enrutamiento"""
    router = GiniRouter()
    
    mock_response = """
    Analizando la arquitectura.
    ```xml
    <enrutar target="fani">
        <mensaje>Crea el frontend en React</mensaje>
    </enrutar>
    <enrutar target="cami">
        <mensaje>Crea la API en FastAPI</mensaje>
    </enrutar>
    ```
    """
    
    # Mocking genai.GenerativeModel.generate_content to avoid API calls
    class MockContent:
        text = mock_response
        
    class MockModel:
        def generate_content(self, *args, **kwargs):
            return MockContent()
            
    # Inyectamos el mock directamente
    router.model = MockModel()
    
    decision = router.analyze_intent("Desarrollar app fullstack")
    
    assert decision["action"] == "route_multiple"
    assert len(decision["targets"]) == 2
    assert decision["targets"][0]["agent"] == "fani"
    assert "React" in decision["targets"][0]["message"]
    assert decision["targets"][1]["agent"] == "cami"
    assert "FastAPI" in decision["targets"][1]["message"]

def test_gini_router_respond():
    """Prueba el comportamiento de respuesta directa (conversación)"""
    router = GiniRouter()
    
    mock_response = """
    <responder>
        <mensaje>¡Hola! Soy Gini V8.0. ¿En qué te puedo ayudar hoy?</mensaje>
    </responder>
    """
    
    class MockContent:
        text = mock_response
        
    class MockModel:
        def generate_content(self, *args, **kwargs):
            return MockContent()
            
    router.model = MockModel()
    decision = router.analyze_intent("Hola")
    
    assert decision["action"] == "respond"
    assert "Gini V8.0" in decision["message"]
