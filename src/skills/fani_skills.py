# Fani Skills
# Herramientas exclusivas del Frontend Developer (UI/UX)

def check_accessibility(html_snippet: str) -> list:
    """Escanea un snippet HTML buscando faltas de accesibilidad comunes."""
    warnings = []
    if "<img" in html_snippet and "alt=" not in html_snippet:
        warnings.append("Alerta A11y: Una etiqueta <img> no tiene el atributo 'alt'.")
    if "<button" in html_snippet and "aria-label" not in html_snippet and ">" + "</button>" in html_snippet: # Simplified check for empty button
        warnings.append("Alerta A11y: Un botón podría no tener texto descriptivo ni 'aria-label'.")
    return warnings

def generate_react_component(component_name: str, has_props: bool = True) -> str:
    """Genera un esqueleto de componente funcional de React con buenas prácticas."""
    props_str = "{ props }" if has_props else ""
    return f"""import React from 'react';
import './{component_name}.css';

const {component_name} = ({props_str}) => {{
  return (
    <div className="{component_name.lower()}-container">
      {/* Contenido UI deslumbrante aquí */}
    </div>
  );
}};

export default {component_name};
"""
