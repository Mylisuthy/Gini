# Sistema Multi-Agente Corporativo: Manual de Usuario V5.1

¡Bienvenido al ecosistema **Gini V5.1**! Esta plataforma es un Hub de Inteligencia Artificial open-source y auto-instalable, diseñado para orquestar un equipo de agentes virtuales (Swarm AI) que pueden programar, gestionar y ejecutar comandos en tu entorno local.

---

## 1. Inicio Rápido y Configuración

El ecosistema es *Zero-Code*, lo que significa que no necesitas modificar código Python para configurarlo o escalarlo.

1. **Abrir la Plataforma:** Ejecuta `start.bat`. Se abrirá la interfaz gráfica de escritorio.
2. **Cargar Credenciales Seguras:**
   - Ve a la pestaña superior derecha llamada **"Seguridad"**.
   - Ingresa tu `GEMINI_API_KEY` (Obligatorio) y los datos de Azure DevOps (Opcional, solo si usarás a Yimi para gestionar Backlog).
   - Haz clic en **Guardar Configuración Cifrada**. 
   - *Nota de Privacidad:* Tus credenciales se cifran asimétricamente mediante la librería `cryptography` y se almacenan localmente en `.env_secure`.

---

## 2. El Chat Central (Operaciones)

En esta pestaña interactúas con **Gini (🧠)**, la Router Principal.
Gini no hace el trabajo pesado, ella *enruta*.

- **Comportamiento:** Si le preguntas "¿Cómo estás?", ella responderá directamente. Si le pides "Necesito que crees una API con FastAPI", Gini invocará silenciosamente a un especialista (por ejemplo, a Tobi o a Cami) y te traerá su plan de acción.
- **Acciones y Human-In-The-Loop:**
  - Los agentes nunca ejecutan código sin tu permiso.
  - Cuando un agente propone una solución, verás una caja de cristal ("Acción") con el código, los archivos a modificar, o los **Comandos de Terminal** a ejecutar.
  - Tienes dos botones: **[Aprobar y Ejecutar]** o **[Rechazar]**.
  - Si apruebas, la aplicación se bloquea brevemente (mostrando un círculo de carga) para evitar envíos dobles, mientras el "Motor Universal" crea los archivos físicamente en `src/workspace/` y/o ejecuta los comandos de terminal en tu PC.

---

## 3. El Laboratorio de Evolución (Evo)

**Evo (🧬)** es tu Arquitecto de Sistemas. Este meta-agente tiene acceso a los "Cerebros" (System Prompts) de los demás agentes.

### Crear un Agente Nuevo
Para escalar tu equipo de IA sin escribir código, simplemente habla con Evo:
- **Tú:** *"Crea un agente llamado Max, experto en C++ y Bases de Datos SQL."*
- **Evo:** Analizará la arquitectura y te presentará una "Matriz de Personalidad". Si apruebas e inyectas el conocimiento, el agente nace instantáneamente. ¡Gini podrá asignarle tareas en ese mismo momento!

### Probar un Agente
Para no arruinar el ecosistema con agentes defectuosos, puedes probarlos en Evo antes de usarlos:
- **Tú:** *"Prueba a Max pidiéndole que cree una tabla en SQL."*
- **Evo:** Simulará la invocación de Max y te mostrará el output JSON crudo (sin ejecutar nada en tu PC). Así podrás validar si sus Skills están funcionando bien.

### Purgar un Agente
Si un agente se vuelve obsoleto o defectuoso, elimínalo permanentemente.
- **Tú:** *"Elimina al agente Max."*
- Evo te pedirá confirmación con un botón rojo. Al purgarlo, Gini dejará de conocerlo y su personalidad será borrada.

---

## 4. Características Visuales V5.1
El diseño UI utiliza el estándar **Glassmorphism**, con cajas semitransparentes sobre fondos gradientes oscuros. Durante el procesamiento, observarás barras de carga, bloqueos de inputs y efectos *hover* para garantizar que siempre sepas qué está haciendo el sistema y no generes colisiones de red.
