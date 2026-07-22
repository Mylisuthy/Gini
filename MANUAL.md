# Manual de Operación Gini OS (Arquitectura Unify)

¡Bienvenido al ecosistema **Gini OS**! Esta plataforma auto-instalable materializa la **Arquitectura Unify**, la cual orquesta un equipo de agentes virtuales (Swarm AI) que trabajan concurrentemente sin un cuello de botella central, a través de una **Pizarra Compartida**.

---

## 1. Configuración Inicial e Inicio Rápido

El ecosistema es nativo en Python y cuenta con filosofía **Zero-Node** (sin instalaciones pesadas de NodeJS).

1. **Cargar Credenciales:** En la raíz del proyecto, edita o crea un archivo `.env` con:
   - `GEMINI_API_KEY="tu-llave"` (Requerido para el motor de la IA).
   - `TAVILY_API_KEY="tu-llave"` (Opcional, para búsquedas en la web profesional).
2. **Abrir la Plataforma:** Ejecuta `start.bat`. Esto levantará el servidor FastAPI en el puerto 8000.
3. Ingresa desde tu navegador a `http://127.0.0.1:8000`. Verás la nueva interfaz inmersiva *Glassmorphism*.

---

## 2. Operativa Visual en el Dashboard

Tu nueva interfaz de control se divide en dos vistas principales:

### Vista Chat (Enrutador Gini)
Aquí envías las órdenes generales corporativas. Gini ya **no** asignará las tareas a un programador directo. Actúa como un muro de contención:
- Tú escribes: *"Necesitamos un portal de pagos."*
- Gini clasifica el alcance y lo empuja hacia el **Product Owner (Yimi)**.
- Gini te informará que el proceso fue "encolado" exitosamente.

### Vista Pizarra Compartida (Blackboard / Kanban)
Es el verdadero corazón de Unify (`backlog_state.json`). 
- **Auto-Sincronización:** La pantalla consultará automáticamente cada 5 segundos al servidor.
- **Flujo Upstream:** Verás cómo Yimi crea un Epic, lo desglosa y lo arroja a la columna `READY_FOR_DEV`.
- **Flujo Downstream (P2P):** Los líderes como **Cami** leerán la columna `READY_FOR_DEV`, tomarán la tarea pasándola a `IN_PROGRESS` (bloqueándola para otros) y, cuando terminen de programar, la dejarán en `READY_FOR_QA`.
- **Aseguramiento de Calidad:** Verás a Mani tomar la tarea. Si la aprueba pasa a `DONE`. Si encuentra un fallo de seguridad, la devuelve como `REJECTED_BY_QA` y Cami debe repetirla. ¡Todo automatizado!

---

## 3. Seguridad Perimetral: Sandbox "Zero-Trust"

Durante su ciclo de trabajo (ReAct), los agentes técnicos van a intentar ejecutar el código Python que generen usando la orden `<ejecutar_codigo>`.

El sistema cuenta con un escudo protector dual de la máquina Host:
1. **Docker (Recomendado):** Si el agente detecta que tienes Docker, correrá sus ensayos en un contenedor efímero aislado sin acceso a la red ni al disco.
2. **Fallback Estricto (Local):** Si no hay Docker (como un entorno Windows local estándar), aislará el subproceso purgando llaves API confidenciales de la RAM y hackeando módulos como `subprocess` e inhabilitándolos para que ningún modelo loco pueda ejecutar un `rm -rf` o descargar malware.

---

## 4. Evolución de Agentes y Memoria RAG

El flujo corporativo se enriquece con:
- **Auto-Evolución (Evo):** Los agentes solicitan modificaciones de "ADN" a sí mismos si carecen de instrucciones en sus `prompt.xml`.
- **Ingesta RAG (Dori):** Los agentes pueden detenerse a leer manuales de tu repositorio haciendo uso de almacenamiento Vectorial en Qdrant para tener un contexto infinito.
