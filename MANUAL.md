# Sistema Multi-Agente Corporativo: Manual de Usuario V8.0

¡Bienvenido al ecosistema **Gini V8.0**! Esta plataforma es un Hub de Inteligencia Artificial open-source y auto-instalable, diseñado para orquestar un equipo de agentes virtuales (Swarm AI) que pueden programar, gestionar, investigar y auto-evolucionar en tu entorno local mediante un flujo de trabajo paralelo.

---

## 1. Inicio Rápido y Configuración Segura

El ecosistema es *Zero-Code* en su núcleo, lo que significa que no necesitas modificar código Python para configurarlo o escalarlo, los agentes de IA lo hacen por ti.

1. **Abrir la Plataforma:** Ejecuta `start.bat`. Se abrirá la interfaz gráfica.
2. **Cargar Credenciales Seguras:**
   - Ve a la pestaña de **"Seguridad"**.
   - Ingresa tu `GEMINI_API_KEY` (Motor lógico principal).
   - Ingresa tu `TAVILY_API_KEY` (Motor de búsqueda web profesional para agentes).
   - Haz clic en **Guardar Configuración Cifrada**. 
   - *Nota de Privacidad:* Tus credenciales se cifran asimétricamente mediante la librería `cryptography` y se almacenan localmente en `.env_secure`. Nunca viajan sin protección.

---

## 2. El Chat Central (Operaciones Paralelas y Herramientas)

En esta pestaña interactúas con **Gini (🧠)**, la Lead Architect.

- **Comportamiento Asincrónico:** Si le pides construir un proyecto entero, Gini no lo hará sola. Emitirá múltiples órdenes y enrutará en *paralelo* a los especialistas (Fani, Cami, Mani).
- **Ciclo ReAct y Uso de Herramientas (NUEVO):** Los agentes ahora imitan el razonamiento humano. Antes de darte una respuesta final, pueden hacer "pausas" automáticas para:
  - Consultar manuales cargados masivamente en la memoria vectorial (`Qdrant`).
  - Buscar información actualizada en internet usando `Tavily`.
  - Levantar un **Sandbox Efímero de Docker** para probar el código Python que acaban de escribir y asegurar que funciona antes de mostrártelo.
- **Auto-Reflexión (QA Interno):** Cuando los agentes terminan, verás un bloque amarillo en sus tarjetas (`<reflexion>`). El sistema les obliga a criticar su propio código y corregir fallos antes de entregártelo.
- **Acciones (Human-In-The-Loop):** Tienes dos botones: **[Aprobar y Ejecutar]** o **[Rechazar]**.

---

## 3. El Laboratorio de Evolución y Base de Conocimientos

### Evolución Desatendida (La Magia de la V8.0)
Si durante una operación normal un agente detecta que no tiene los conocimientos necesarios, lanzará una alerta `<auto_evolucion>`. **Evo se ejecutará en segundo plano**, modificará el código fuente del agente (`cami_prompt.xml`), inyectará la regla permanente y te avisará que la mutación fue exitosa.

### Ingesta Masiva de Documentos (RAG Pipeline)
Para inyectar conocimiento a todo el enjambre de una sola vez, puedes soltar archivos PDF, Word o Texto en la carpeta de procesamiento. El Pipeline de Ingesta particionará (Chunking), vectorizará y guardará esta información en la Base de Datos Local (Qdrant). Los agentes podrán consultarla activamente cuando sientan que les falta contexto.

---

## 4. Características Visuales V8.0 (Hacia la Arquitectura Zero-Node)
El diseño UI se encuentra en transición hacia un enfoque **Zero-Node**, lo cual permitirá renderizar interfaces súper avanzadas (React/Tailwind) servidas nativamente desde Python sin requerir que instales herramientas de NodeJS pesadas, garantizando interacciones fluidas mientras el enjambre procesa gigabytes de contexto.
