# Gini V8.0: Ecosistema Multi-Agente Corporativo 🚀

![Version](https://img.shields.io/badge/version-8.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![Architecture](https://img.shields.io/badge/architecture-parallel%20XML-orange.svg)

Bienvenido a **Gini V8.0**, un Hub de Inteligencia Artificial open-source que implementa una arquitectura avanzada de *Enjambre Paralelo (Swarm AI)*. Diseñado para orquestar un equipo de agentes virtuales capaces de programar, gestionar, realizar control de calidad (Auto-QA) y auto-evolucionar de manera completamente autónoma.

---

## 🌟 Características Principales (V8.0)

1. **Orquestación Paralela (Multithreading):** Gini, como Lead Architect, puede dividir un requerimiento complejo (ej. "Construye un backend y un frontend a la vez") y enrutar las tareas a múltiples agentes (Cami y Fani) simultáneamente en hilos separados sin bloquear la interfaz.
2. **Protocolo de Comunicación XML 7D:** El sistema abandonó las estructuras obsoletas (JSON/Markdown) para pasar a un estándar nativo en XML. Las comunicaciones internas son veloces, estandarizadas y libres de errores de sintaxis.
3. **Auto-QA (Cadena de Pensamiento):** Cada agente cuenta con un protocolo estricto de auto-crítica (`<reflexion>`). Antes de entregar código, los agentes analizan su solución internamente, aplican reglas de negocio (ej. SOLID, WCAG) y se corrigen a sí mismos.
4. **Auto-Evolución Desatendida (Evo):** Si un especialista se topa con un muro de conocimiento (ej. una librería nueva), levanta una alerta `<auto_evolucion>`. El Arquitecto (Evo) se inicializa en segundo plano, reprograma la matriz XML del agente fallido inyectando permanentemente el nuevo conocimiento, y lo guarda en disco de forma invisible.

---

## 🏗️ La Estructura del Equipo (Swarm)

* **🧠 Gini:** Router Principal. Lee tus intenciones, y decide si contestar o *enrutar* el trabajo en paralelo a los demás agentes.
* **🧬 Evo:** Meta-Agente Arquitecto. Puede leer, crear, modificar y eliminar las matrices de personalidad (archivos XML) de los demás agentes.
* **🛠️ Especialistas Activos:**
    * **Yimi:** System Analyst / Product Owner.
    * **Fani:** Frontend Developer.
    * **Cami:** Backend Developer.
    * **Mani:** QA Automation Engineer.
    * **Romi:** DevOps / SecOps Engineer.
    * **Sefi:** Especialista en Bases de Datos.
    * **Tobi:** Fullstack Generalista.

---

## 🚀 Inicio Rápido

1. **Clonar el repo:**
   ```bash
   git clone https://github.com/Mylisuthy/Gini.git
   cd Gini
   ```

2. **Entorno Virtual (Recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Nota: Asegúrate de tener flet, google-genai, cryptography, python-dotenv).*

4. **Ejecutar:**
   ```bash
   start.bat
   # O directamente: python src/gui/app.py
   ```

---

## 🔒 Configuración Segura
Ve a la pestaña superior derecha **"Seguridad"** en la aplicación e ingresa tu `GEMINI_API_KEY`. Tus credenciales se cifran de extremo a extremo usando criptografía asimétrica y se guardan localmente.

---

*Desarrollado y mantenido con estándares de arquitectura corporativa.*
