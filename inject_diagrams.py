import sys

def inject_diagrams():
    with open('BacklogCaracteristics.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    diag1 = """
```mermaid
graph TD
    A[Celsia Product Backlog<br/>Nodo de Gestión] --> B(Work Items Centralizados)
    B --> |Iniciativas, US, Bugs| C{Proyectos Técnicos<br/>Nodos de Ejecución}
    C --> D[Producto A: Repos, Pipelines, Test Plans]
    C --> E[Producto B: Repos, Pipelines, Test Plans]
```
"""

    diag2 = """
```mermaid
graph TD
    P[Producto o Servicio<br/>Portafolio] --> I[Iniciativa<br/>Funcionalidad]
    I --> U[User Story<br/>Ejecución]
    I --> B[Bug<br/>Ejecución]
    I --> D[Deployment<br/>Ejecución]
    U --> T[Task<br/>Tarea - Max 8h]
    B --> T2[Task]
```
"""

    diag3 = """
```mermaid
stateDiagram-v2
    [*] --> Nuevo
    Nuevo --> Activo : Inicia Análisis/Desarrollo
    Activo --> Pruebas : Despliegue en UAT
    Pruebas --> Completado : Aprobación Funcional
    Nuevo --> Cancelado : Visto Bueno PO
    Activo --> Cancelado
```
"""

    diag4 = """
```mermaid
gitGraph
    commit id: "Producción"
    branch Develop
    commit id: "Integración"
    branch F1355_Login
    commit id: "Desarrollo Task"
    checkout Develop
    merge F1355_Login
    checkout main
    merge Develop tag: "Release 1.2"
```
"""

    if 'graph TD' not in content:
        content = content.replace('## 2. Arquitectura de "Doble Nodo" en Azure DevOps\n', '## 2. Arquitectura de "Doble Nodo" en Azure DevOps\n' + diag1)
        content = content.replace('## 3. Jerarquía de Trabajo y Definiciones\n', '## 3. Jerarquía de Trabajo y Definiciones\n' + diag2)
        content = content.replace('## El Estado (state)\n', '## El Estado (state)\n' + diag3)
        content = content.replace('Branches (Rama)\n', 'Branches (Rama)\n' + diag4)

        with open('BacklogCaracteristics.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Diagrams injected.")
    else:
        print("Diagrams already injected.")

if __name__ == '__main__':
    inject_diagrams()
