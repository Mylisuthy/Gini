# Gini OS: Ecosistema Multi-Agente Corporativo 🚀 (Arquitectura Unify)

![Version](https://img.shields.io/badge/version-Unify%201.0-blue.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![Architecture](https://img.shields.io/badge/architecture-Zero--Node%20P2P-orange.svg)

Bienvenido a **Gini OS**, un Sistema Operativo Corporativo gestionado por una Organización Autónoma Descentralizada de Agentes Inteligentes (Swarm AI). Diseñado para orquestar un equipo de agentes que pueden programar, gestionar y validar bajo la filosofía de "Zero-Trust" y comunicación "Peer-to-Peer" (P2P).

---

## 🌟 Arquitectura "Unify" (Novedades)

1. **Gini (Enrutador Semántico):** Gini ha dejado de ser una asignadora de tareas técnicas. Ahora opera como un guardián semántico que recibe tus requerimientos, los empaqueta como Épicas y los envía obligatoriamente al Product Owner (Yimi) para iniciar el ciclo *Upstream*.
2. **Pizarra Compartida (Blackboard):** Reemplaza el cuello de botella centralizado. Ahora, el estado global vive en un Kanban (`backlog_state.json`). Todos los agentes técnicos leen y escriben en esta pizarra compartida para sincronizarse sin chocar entre sí (Exclusión Mutua).
3. **Comunicación Peer-to-Peer (Handoff):** Los líderes de desarrollo (Cami/Fani) no hablan con Gini al terminar. Cuando el código está listo, cambian el estado en el Blackboard a `READY_FOR_QA` y "despiertan" directamente al equipo de Aseguramiento de Calidad (Mani) estableciendo bucles de mejora continuos.
4. **Sandbox de Ejecución Segura (Zero-Trust):** Cuando los agentes técnicos escriben código, lo prueban usando un Sandbox Inteligente. Si Docker está instalado, levantan contenedores efímeros sin red. Si no lo está, activan un entorno local *Restringido Estricto* que envenena bibliotecas letales (ej. `subprocess`) y borra variables de entorno (`API_KEYS`) de memoria para proteger tu equipo.
5. **Arquitectura Visual Zero-Node:** Cero dependencias pesadas de NPM/Node.js. El servidor es un API asíncrona ultra ligera en **FastAPI** que sirve un frontend premium en HTML/JS/CSS *Vanilla* con diseño Glassmorphism y Dark Mode vibrante.

---

## 🏗️ La Estructura del Enjambre (Swarm)

* **🧠 Gini:** Router Principal. Lee intenciones, empaqueta el requerimiento y se lo pasa a Yimi.
* **💼 Yimi:** Product Owner. Desglosa las solicitudes en Historias de Usuario y Tareas, escribiendo directamente en el Blackboard.
* **🛠️ Especialistas Activos (Consumidores del Blackboard):**
    * **Fani:** Frontend Developer. Toma tareas de la pizarra.
    * **Cami:** Backend Developer. Capaz de ejecutar código en Sandbox Seguro.
    * **Mani:** QA Automation Engineer. Recibe el código, lo prueba implacablemente y puede rechazarlo devolviéndoselo a Cami.
* **🧬 Evo & Dori:** Mantenimiento estructural y Base de Datos Vectorial Semántica (RAG local).

---

## 🚀 Inicio Rápido

La arquitectura *Zero-Node* permite arrancar todo con un doble clic en entornos Windows:

1. **Clonar el repo:**
   ```bash
   git clone https://github.com/Mylisuthy/Gini.git
   cd Gini
   ```

2. **Configuración Segura (Ciberseguridad):**
   Crea un archivo `.env` en la raíz del proyecto y añade:
   ```env
   GEMINI_API_KEY="tu_llave"
   TAVILY_API_KEY="tu_llave"
   ```

3. **Ejecutar (Arranque Mágico):**
   Simplemente ejecuta el orquestador:
   ```cmd
   start.bat
   ```
   El script creará el entorno virtual, instalará requerimientos (FastAPI, Uvicorn, etc.), levantará el Backend y dejará la interfaz gráfica lista para que entres a `http://127.0.0.1:8000`.

---

*Desarrollado en Celsia con estándares de arquitectura corporativa "Shift-Left" y "DevSecOps".*
