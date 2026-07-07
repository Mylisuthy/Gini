# Sistema Multi-Agente Corporativo: Manual de Usuario V8.0

¡Bienvenido al ecosistema **Gini V8.0**! Esta plataforma es un Hub de Inteligencia Artificial open-source y auto-instalable, diseñado para orquestar un equipo de agentes virtuales (Swarm AI) que pueden programar, gestionar y auto-evolucionar en tu entorno local mediante un flujo de trabajo paralelo.

---

## 1. Inicio Rápido y Configuración

El ecosistema es *Zero-Code* en su núcleo, lo que significa que no necesitas modificar código Python para configurarlo o escalarlo, los agentes de IA lo hacen por ti.

1. **Abrir la Plataforma:** Ejecuta `start.bat`. Se abrirá la interfaz gráfica de escritorio.
2. **Cargar Credenciales Seguras:**
   - Ve a la pestaña superior derecha llamada **"Seguridad"**.
   - Ingresa tu `GEMINI_API_KEY` (Obligatorio) y los datos de Azure DevOps (Opcional, solo si usarás a Yimi para gestionar Backlog).
   - Haz clic en **Guardar Configuración Cifrada**. 
   - *Nota de Privacidad:* Tus credenciales se cifran asimétricamente mediante la librería `cryptography` y se almacenan localmente en `.env_secure`.

---

## 2. El Chat Central (Operaciones Paralelas)

En esta pestaña interactúas con **Gini (🧠)**, la Lead Architect.

- **Comportamiento Asincrónico:** Si le pides construir un proyecto entero, Gini no lo hará sola. Ella emitirá múltiples órdenes y enrutará en *paralelo* a los especialistas (Fani, Cami, Mani). Verás múltiples tarjetas cargando simultáneamente.
- **Auto-Reflexión (QA Interno):** Cuando los agentes terminan, verás un bloque amarillo en sus tarjetas. Esto es su *Cadena de Pensamiento*. El sistema les obliga a criticar su propio código y corregir fallos antes de entregártelo.
- **Acciones (Human-In-The-Loop):**
  - Tienes dos botones: **[Aprobar y Ejecutar]** o **[Rechazar]**.
  - Si apruebas, el "Motor Universal" crea los archivos físicamente con las rutas especificadas y/o ejecuta los comandos de terminal (como correr pruebas o levantar servidores locales).

---

## 3. El Laboratorio de Evolución (Evo Autónomo)

**Evo (🧬)** es tu Arquitecto de Sistemas. Opera bajo el nuevo **Protocolo XML 7D**.

### Evolución Desatendida (La Magia de la V8.0)
Si durante una operación normal en el Chat Central, un agente detecta que no tiene los conocimientos necesarios (Ej. Cami no sabe usar una librería específica de Python), el agente lanzará una alerta `<auto_evolucion>`. 
Sin que intervengas, **Evo se ejecutará en segundo plano**, modificará el código fuente del agente (`cami_prompt.xml`), inyectará la regla permanente y te avisará que la mutación fue exitosa.

### Crear / Modificar Manualmente
Para escalar tu equipo de IA, simplemente ve a la pestaña del Laboratorio y habla con Evo:
- **Tú:** *"Crea un agente llamado Max, experto en C++ y Bases de Datos SQL."*
- **Evo:** Generará la nueva matriz XML y la guardará físicamente. Gini lo detectará al instante para futuras tareas.

---

## 4. Características Visuales V8.0
El diseño UI utiliza el estándar **Glassmorphism**. Durante el procesamiento de múltiples agentes, el entorno no se congela gracias a la reestructuración en hilos (`threading`), garantizando interacciones fluidas mientras el enjambre procesa gigabytes de contexto.
