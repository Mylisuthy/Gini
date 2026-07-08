# Contexto de Diseño UI/UX - Gini V8.0 (Swarm AI)

Este documento sirve como "Cerebro de Contexto" para el diseño de prototipos visuales (Figma, Adobe XD, o código Flet). Define la realidad arquitectónica del sistema para que la nueva interfaz gráfica represente fielmente la potencia del backend.

## 1. Naturaleza del Sistema
Gini V8.0 **no es un chatbot tradicional**. Es un **entorno de desarrollo paralelo de Inteligencia Artificial**. La interfaz debe sentirse como el panel de control de una corporación donde múltiples empleados (agentes) trabajan a la vez, no como un chat lineal estilo WhatsApp.

## 2. El Flujo de Usuario (User Journey)

1. **Ingreso del Requerimiento:** El usuario escribe un prompt en la barra inferior (ej. "Construye el frontend y backend de una calculadora").
2. **Análisis de Orquestación (Gini):** Gini (Lead Architect) procesa la orden y decide la ruta. La UI debe mostrar un mensaje jerárquico de Gini anunciando a quiénes va a invocar.
3. **Carga Paralela Asincrónica:** Si Gini enruta a Fani y Cami, la UI debe renderizar **dos tarjetas visuales independientes simultáneamente**, mostrando un indicador de carga ("FANI procesando código...", "CAMI procesando código..."). **El sistema NUNCA se congela**.
4. **Entrega de Resultados (Tarjetas de Acción):** Una vez que un agente termina, su tarjeta se expande mostrando:
   - **Bloque de Auto-Reflexión (Obligatorio):** Un bloque visualmente destacable (idealmente estilo "Warning" o nota amarilla) donde el agente critica su propio código antes de entregarlo.
   - **Estrategia:** Texto descriptivo de la solución.
   - **Código Fuente:** Bloques de código formateados (HTML, Python, etc.).
5. **Control Humano (Human-In-The-Loop):** Al final de cada tarjeta, deben existir botones de decisión crítica: **[Aprobar y Ejecutar]** y **[Rechazar]**.
6. **Ejecución Física:** Si el usuario aprueba, se ejecutan comandos en el PC local y se muestran logs de terminal incrustados en la tarjeta (éxito en verde, errores de compilación en rojo).

## 3. Alertas Críticas (Auto-Evolución)
Ocasionalmente, un agente puede fallar o detectar que le falta conocimiento. En ese caso emitirá una "Alerta de Auto-Evolución". 
- **Requisito UI:** Esta alerta debe romper el patrón visual (color naranja/rojo) pidiendo permiso para invocar a EVO. Si el usuario aprueba, la UI debe mostrar que EVO está reprogramando al agente en segundo plano.

---

## 4. Los Actores del Sistema (El Enjambre)
El diseño debe contemplar avatares, iconos o esquemas de colores distintivos para cada uno de estos agentes, ya que pueden aparecer varios a la vez en pantalla.

### 👑 El Núcleo de Control
*   **Gini (Router Principal):** La jefa. Analiza intenciones. Su voz es directiva y corporativa.
*   **Evo (Arquitecto de Mutación):** Trabaja en el "Laboratorio". No hace código de usuario, reprograma el cerebro XML de los otros agentes.

### 🛠️ Los Especialistas (Trabajadores Paralelos)
*   **Yimi (Product Owner):** Crea Historias de Usuario, Sprints y Backlogs (Formato Azure DevOps). Su salida suele ser JSON estructurado y tablas de planificación.
*   **Fani (Frontend Developer):** Obsesionada con la accesibilidad (WCAG) y el diseño. Produce HTML, CSS, React, Flet.
*   **Cami (Backend Developer):** Arquitecta estricta. Produce Python, Node, APIs. Siempre usa principios SOLID y patrones de diseño.
*   **Mani (QA Automation):** El destructor de código. Escribe scripts de Cypress, Pytest, Jest. Su trabajo es hacer pruebas de estrés.
*   **Romi (DevSecOps):** Experta en despliegues. Escribe Dockerfiles, YAML de CI/CD, scripts de bash. Obsesionada con la seguridad (Zero Trust).
*   **Sefi (Data Engineer):** Diseña bases de datos SQL/NoSQL, esquemas ER y queries de alta eficiencia.
*   **Tobi (Fullstack General):** El comodín. Resuelve tareas rápidas o scripts sueltos que no encajan en una especialidad estricta.

## 5. Requisitos de Componentes Visuales para el Prototipo

Para que tu diseño se adapte al código actual, asegúrate de diseñar los siguientes componentes:

1. **Panel Principal (Scrollable):** Donde se apilan las tarjetas.
2. **Action Card (Tarjeta Hija):** Contenedor que agrupa la respuesta de 1 agente.
3. **Markdown Renderer:** Un área tipográfica para leer texto enriquecido, negritas, tablas.
4. **Code Snippet Block:** Un contenedor oscuro para código fuente, idealmente con botón de "Copiar".
5. **Estado de Ejecución (Terminal Overlay):** Un área estilo consola de comandos que muestre texto plano de lo que está ocurriendo en la máquina física al oprimir "Aprobar".
6. **Tabs Superiores:** La navegación principal (Actualmente: "Chat Central", "Laboratorio Evo", "Seguridad").
