import pytest
import sys
import os

# Asegurar importación de src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gui.app import premium_button, COLORS
from src.core.universal_agent import UniversalAgent
import flet as ft

def test_premium_button_builder():
    """
    Verifica que el constructor de botones premium no use atributos
    deprecated de Flet (como ft.colors.WHITE o ft.icons.SEND) y genere un ElevatedButton correcto.
    """
    # Usar strings literales nos protege de caídas por versiones de Flet
    btn = premium_button(
        text="Test Button",
        base_color="#123456",
        hover_color="#654321",
        on_click=lambda e: None,
        icon="send"
    )
    
    assert isinstance(btn, ft.ElevatedButton)
    assert btn.content == "Test Button"
    assert btn.icon == "send"
    # Verificar que el estilo usa strings en lugar de constantes de módulo
    assert btn.style.color == "white"

def test_color_palette_consistency():
    """
    Verifica que la paleta corporativa tenga las llaves necesarias.
    """
    required_keys = ["gini", "yimi", "tobi", "evo", "bg_start", "bg_end", "glass"]
    for key in required_keys:
        assert key in COLORS
        
def test_universal_agent_initialization():
    """
    Verifica que el agente universal pueda instanciarse sin fallar.
    """
    agent = UniversalAgent("test_agent")
    assert agent.agent_name == "test_agent"

def test_create_glass_container():
    """
    Verifica que el constructor de contenedores no lance errores por ft.Border.all()
    """
    from src.gui.app import create_glass_container
    dummy_text = ft.Text("Dummy")
    container = create_glass_container(dummy_text)
    
    assert isinstance(container, ft.Container)
    # Si ft.Border.all falla, la instanciación de arriba lanzará una excepción
    assert container.content == dummy_text

