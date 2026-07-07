import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui.app import main

def test_full_ui_initialization():
    """
    Evalúa la función main() completa usando un mock de la página.
    Esto revelará CUALQUIER error de atributo en la librería flet 
    (como ft.Alignment.TOP_CENTER, ft.MainAxisAlignment, etc.)
    que pueda suceder durante el renderizado.
    """
    mock_page = MagicMock()
    # Mockear las propiedades para evitar problemas con la asignación
    mock_page.overlay = []
    
    # Ejecutamos la función principal
    main(mock_page)
    
    # Si la ejecución llega aquí, significa que no hubo ningún AttributeError 
    # relacionado a la versión de la librería Flet en el layout inicial.
    assert True
