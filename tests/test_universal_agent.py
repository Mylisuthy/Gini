import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.universal_agent import UniversalAgent

@patch('src.core.universal_agent.genai.GenerativeModel')
def test_universal_agent_xml_parsing(MockModel):
    """Prueba que el UniversalAgent extrae correctamente las etiquetas del XML 7D"""
    agent = UniversalAgent("cami")
    
    mock_response = """
    ```xml
    <reflexion>Debo usar la librería math para esta operación.</reflexion>
    <explicacion>Se implementó la función utilizando principios SOLID.</explicacion>
    <archivo path="calculos.py">
def sumar(a, b):
    return a + b
    </archivo>
    <comando>
python calculos.py
    </comando>
    ```
    """
    
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value = MagicMock(text=mock_response)
    MockModel.return_value = mock_instance
    
    # generate_plan no ejecuta los comandos, solo parsea y devuelve el dict
    plan = agent.generate_plan("Suma 2+2 en calculos.py")
    
    assert "error" not in plan
    assert plan["reflexion"] == "Debo usar la librería math para esta operación."
    assert plan["explicacion"] == "Se implementó la función utilizando principios SOLID."
    assert len(plan["archivos"]) == 1
    assert plan["archivos"][0]["nombre"] == "calculos.py"
    assert "def sumar" in plan["archivos"][0]["contenido"]
    assert len(plan["comandos"]) == 1
    assert plan["comandos"][0].strip() == "python calculos.py"

@patch('src.core.universal_agent.genai.GenerativeModel')
def test_universal_agent_fallback_parsing(MockModel):
    """Prueba que el UniversalAgent maneja salidas corruptas o sin XML correctamente"""
    agent = UniversalAgent("cami")
    
    mock_response = "Esta es una respuesta normal sin etiquetas XML porque hubo un fallo cognitivo."
    
    mock_instance = MagicMock()
    mock_instance.generate_content.return_value = MagicMock(text=mock_response)
    MockModel.return_value = mock_instance
    
    plan = agent.generate_plan("Dime hola")
    
    # El UniversalAgent tiene un fallback que toma la respuesta cruda si no hay comandos ni archivos
    assert "error" not in plan
    assert "explicacion" in plan
    assert plan["archivos"] == []
    assert plan["comandos"] == []
    assert "fallo cognitivo" in plan["explicacion"]
