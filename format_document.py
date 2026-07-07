import sys
import re

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply professional formatting
    
    # Ensure sections are proper headers
    replacements = [
        (r'^1\. Introducción y Visión$', r'## 1. Introducción y Visión'),
        (r'^2\. Arquitectura de "Doble Nodo" en Azure DevOps$', r'## 2. Arquitectura de "Doble Nodo" en Azure DevOps'),
        (r'^2\.1\. Nodo de Gestión: Celsia Product Backlog$', r'### 2.1. Nodo de Gestión: Celsia Product Backlog'),
        (r'^2\.2\. Nodos de Ejecución: Proyectos de Producto$', r'### 2.2. Nodos de Ejecución: Proyectos de Producto'),
        (r'^3\. Jerarquía de Trabajo y Definiciones$', r'## 3. Jerarquía de Trabajo y Definiciones'),
        (r'^4\. Gestión de Capacidad y Clasificación \(Paths\)$', r'## 4. Gestión de Capacidad y Clasificación (Paths)'),
        (r'^4\.1\. Reglas de Asignación de Rutas$', r'### 4.1. Reglas de Asignación de Rutas'),
        (r'^4\.2\. Sprints Centralizados y Capacity$', r'### 4.2. Sprints Centralizados y Capacity'),
        (r'^Recomendaciones para la documentación de las iniciativas:$', r'## Recomendaciones para la documentación de las iniciativas'),
        (r'^Campos para su diligenciamiento:$', r'### Campos para su diligenciamiento'),
        (r'^La descripcion de la iniciativa debe contener:$', r'### La descripcion de la iniciativa debe contener'),
        (r'^El Estado \(state\)$', r'## El Estado (state)'),
        (r'^Tipo de Iniciativa$', r'## Tipo de Iniciativa'),
        (r'^Reglas$', r'### Reglas'),
        (r'^Deployment \(Despliegue\)$', r'## Deployment (Despliegue)'),
        (r'^Task \(Tarea\)$', r'## Task (Tarea)'),
        (r'^Bug \(Hallazgo\)$', r'## Bug (Hallazgo)'),
        (r'^Sintaxis Repositorios \(Git\)$', r'## Sintaxis Repositorios (Git)'),
        (r'^Sintaxis nomenclatura API´s$', r'## Sintaxis nomenclatura API´s'),
        (r'^Esquema de Versionamiento$', r'## Esquema de Versionamiento'),
        (r'^Pipelines$', r'## Pipelines'),
        (r'^Build$', r'### Build'),
        (r'^Releases \(CD\)$', r'### Releases (CD)'),
        (r'^Modulo Library en Pipelines$', r'## Modulo Library en Pipelines'),
        (r'^Test Plans$', r'## Test Plans'),
        (r'^Pruebas Exploratorias$', r'### Pruebas Exploratorias'),
        (r'^Pruebas de Aceptación$', r'### Pruebas de Aceptación')
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content, flags=re.MULTILINE)
        
    # Build Table of Contents
    toc = "# Manual de Arquitectura y Gestión DevSecOps (Celsia)\n\n## Índice de Contenidos\n"
    toc += "- [1. Introducción y Visión](#1-introducción-y-visión)\n"
    toc += "- [2. Arquitectura de Doble Nodo en Azure DevOps](#2-arquitectura-de-doble-nodo-en-azure-devops)\n"
    toc += "- [3. Jerarquía de Trabajo y Definiciones](#3-jerarquía-de-trabajo-y-definiciones)\n"
    toc += "- [4. Gestión de Capacidad y Clasificación (Paths)](#4-gestión-de-capacidad-y-clasificación-paths)\n"
    toc += "- [5. Documentación de Iniciativas](#recomendaciones-para-la-documentación-de-las-iniciativas)\n"
    toc += "- [6. El Estado (state) y Tipo de Iniciativa](#el-estado-state)\n"
    toc += "- [7. Gestión de Work Items (Task, Bug, Deployment)](#task-tarea)\n"
    toc += "- [8. Nomenclatura Git (Repos y APIs)](#sintaxis-repositorios-git)\n"
    toc += "- [9. Esquema de Versionamiento y Ramas](#esquema-de-versionamiento)\n"
    toc += "- [10. CI/CD (Pipelines y Variables)](#pipelines)\n"
    toc += "- [11. Planes de Pruebas (Test Plans)](#test-plans)\n\n"
    toc += "---\n\n"

    final_content = toc + content

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

if __name__ == '__main__':
    process_file('BacklogCaracteristics.md', 'BacklogCaracteristics.md')
    print("Document restructured successfully.")
