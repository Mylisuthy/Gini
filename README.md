# Gini V8.0: Ecosistema Multi-Agente Corporativo 🚀

![Version](https://img.shields.io/badge/version-8.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![Architecture](https://img.shields.io/badge/architecture-parallel%20XML-orange.svg)

Bienvenido a **Gini V8.0**, un Hub de Inteligencia Artificial open-source que implementa una arquitectura avanzada de *Enjambre Paralelo (Swarm AI)*. Diseñado para orquestar un equipo de agentes virtuales capaces de programar, gestionar, realizar control de calidad (Auto-QA) y auto-evolucionar de manera completamente autónoma.

---

## 🌟 Características Principales (V8.0)

1. **Orquestación Paralela (Multithreading):** Gini, como Lead Architect, puede dividir un requerimiento complejo (ej. "Construye un backend y un frontend a la vez") y enrutar las tareas a múltiples agentes simultáneamente en hilos separados sin bloquear la interfaz.
2. **Sistema de Memoria Híbrida y RAG (NUEVO):** Integración nativa con **Qdrant** (VectorDB local) para almacenamiento semántico y un potente **Pipeline de Ingesta Asíncrona** capaz de procesar masivamente PDFs, Word y Texto plano.
3. **Protocolo de Razonamiento ReAct y Tools (NUEVO):** Los agentes ahora poseen herramientas del mundo real. Durante su razonamiento, pueden pausar su ejecución para buscar en la memoria vectorial (`<buscar_rag>`), hacer consultas directas a la web usando la API de Tavily (`<buscar_web>`), o incluso probar su código Python en un **Sandbox de Docker Efímero** (`<ejecutar_codigo>`) para asegurar máxima calidad antes de la entrega final.
4. **Protocolo de Comunicación XML 7D:** Las comunicaciones internas son veloces, estandarizadas y libres de errores de sintaxis gracias al enrutamiento vía XML puro.
5. **Auto-QA y Auto-Evolución (Evo):** Los agentes aplican reglas de negocio internamente (`<reflexion>`). Si detectan un vacío cognitivo, el Meta-Agente (Evo) reprograma permanentemente sus matrices en segundo plano.

---

## 🏗️ La Estructura del Equipo (Swarm)

* **🧠 Gini:** Router Principal. Lee tus intenciones, y decide si contestar o *enrutar* el trabajo.
* **🧬 Evo:** Meta-Agente Arquitecto. Muta el ADN (archivos XML) de los otros agentes en caliente.
* **🛠️ Especialistas Activos:**
    * **Yimi:** System Analyst / Product Owner.
    * **Fani:** Frontend Developer.
    * **Cami:** Backend Developer (Capaz de ejecutar código en Sandbox Seguro).
    * **Mani:** QA Automation Engineer (Tester riguroso en Docker).
    * **Romi:** DevOps / SecOps Engineer.
    * **Sefi:** Especialista en Bases de Datos.
    * **Tobi:** Fullstack Generalista.

---

## 🚀 Inicio Rápido (Arquitectura Zero-Node)

El proyecto está transicionando hacia una experiencia *Open Source Plug & Play*, donde el frontend y backend se levantan con un solo comando en Python, eliminando la dependencia de compiladores de Node.js.

1. **Clonar el repo:**
   ```bash
   git clone https://github.com/Mylisuthy/Gini.git
   cd Gini
   ```

2. **Entorno Virtual (Recomendado):**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   # Nota: Asegúrate de tener Docker instalado en tu máquina si deseas usar las herramientas de Sandbox.
   ```

4. **Ejecutar:**
   ```bash
   start.bat
   ```

---

## 🔒 Configuración Segura (Ciberseguridad Zero-Trust)
Ve a la pestaña de **Seguridad** en la aplicación e ingresa tus credenciales. El sistema requiere:
- `GEMINI_API_KEY`: Para el motor de LLM.
- `TAVILY_API_KEY`: Para permitir a los agentes realizar búsquedas web profundas.
Tus credenciales se cifran de extremo a extremo usando criptografía asimétrica y se guardan localmente.

---

*Desarrollado y mantenido con estándares de arquitectura corporativa.*
