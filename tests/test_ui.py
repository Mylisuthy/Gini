import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gui.app import main

class MockPage:
    def __init__(self):
        self.title = ""
        self.theme_mode = None
        self.padding = 0
        self.spacing = 0
        self.bgcolor = ""
        self.controls = []
        self.overlay = []

    def add(self, *controls):
        self.controls.extend(controls)

    def update(self):
        pass

def test_ui_initialization():
    """
    Prueba que la interfaz gráfica V8.0 se inicialice sin errores de atributos
    (Ej. ft.border.all -> ft.Border.all).
    Si la UI tiene fallos de clases en Flet, este test fallará instantáneamente.
    """
    mock_page = MockPage()
    
    try:
        main(mock_page)
        # Verificamos que se hayan agregado controles al page (el Row principal)
        assert len(mock_page.controls) > 0
    except AttributeError as e:
        pytest.fail(f"Fallo de atributos en la UI durante inicialización: {e}")
    except Exception as e:
        pytest.fail(f"Excepción inesperada al iniciar la UI: {e}")
