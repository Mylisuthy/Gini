# Cami Skills
# Herramientas exclusivas del Backend Developer (Arquitecto de Lógica)

def validate_database_schema(schema_json: dict) -> bool:
    """Valida que un esquema de BD propuesto contenga llaves primarias válidas."""
    if not isinstance(schema_json, dict):
        return False
        
    # Simulación de validación de esquema
    for table_name, table_def in schema_json.items():
        if "id" not in table_def and "primary_key" not in table_def:
            print(f"Alerta: La tabla {table_name} no tiene llave primaria declarada.")
            return False
    return True

def generate_api_endpoint_scaffold(framework: str, endpoint: str, method: str) -> str:
    """Genera código base para un endpoint seguro."""
    if framework.lower() == "express":
        return f"app.{method.lower()}('{endpoint}', authMiddleware, (req, res) => {{\n  // TODO: Implementar lógica\n  res.json({{ status: 'success' }});\n}});"
    elif framework.lower() == "fastapi":
        return f"@app.{method.lower()}('{endpoint}', dependencies=[Depends(verify_token)])\ndef handle_request():\n    # TODO: Implementar lógica\n    return {{'status': 'success'}}"
    return "# Framework no soportado"
