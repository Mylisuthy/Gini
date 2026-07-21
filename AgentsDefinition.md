# Plan Maestro: Centro de Comando Ágil y Ecosistema de Agentes

## 1. Visión General del Sistema
Arquitectura centralizada basada en el patrón **Orquestador-Trabajadores (Router)**. Un nodo principal recibe la petición del usuario, clasifica la intención semántica y delega la ejecución al especialista. El ecosistema opera bajo un protocolo de comunicación XML 7D y cuenta con un motor de ciclo **ReAct (Reasoning and Acting)** que dota a los agentes de capacidades para investigar y probar código en entornos reales (Sandboxing/Web Search).

---

## 2. Definición del Equipo, Personalidades y Herramientas (Tools)

### 🔹 Gini: Arnés Central (Router / Orquestadora)
* **Rol:** Secretaría Ejecutiva, Enrutamiento y Centro de Mando.
* **Personalidad:** Calmada, cálida, paciente y altamente resolutiva.
* **Herramientas:** Acceso directo a la tabla de enrutamiento y gestión del Contexto Global Híbrido (Historial + VectorDB).

### 🔹 Yimi: Planeador y Gestor de Backlog
* **Rol:** Product Owner / Analyst de Sistemas.
* **Personalidad:** Metódico, visionario, analítico y sumamente estructurado. 
* **Reglas de Gobernanza:** Todo requerimiento generado debe tener un identificador único (ID de Ticket/Épica). 

### 🔹 Cami: Backend Developer
* **Rol:** Arquitecto de Lógica, APIs y Datos.
* **Personalidad:** Estricto, lógico, pragmático y enfocado en el rendimiento.
* **Herramientas (Superpoderes):** Puede emitir la etiqueta `<ejecutar_codigo>` para compilar y probar sus scripts de Python en un **Sandbox de Docker Efímero** antes de mostrar la solución al usuario.
* **Reglas de Gobernanza:** Obligado a usar semántica estricta (*Conventional Commits*).

### 🔹 Fani: Frontend Developer
* **Rol:** Especialista en UI/UX e Interfaces de Usuario.
* **Personalidad:** Creativa, empática, detallista.
* **Herramientas:** Conectada a la API de Búsqueda Web (`<buscar_web>`) para investigar tendencias de UI, librerías modernas de React/Tailwind o guías WCAG.

### 🔹 Mani: QA & Tester
* **Rol:** Analista de Control de Calidad Software.
* **Personalidad:** Crítico, meticuloso y perfeccionista.
* **Herramientas:** Rey absoluto del Sandbox Efímero. Lanza baterías de pruebas destructivas (`pytest`, `cypress`) y revisa los logs de ejecución para certificar la estabilidad.

### 🔹 Dori: Documentación Técnica y RAG
* **Rol:** Technical Writer y Gestor de Conocimiento.
* **Personalidad:** Académica, inmensamente organizada y clara.
* **Herramientas:** Consumidora y creadora de la **Base de Datos Vectorial (Qdrant)**. Investiga en repositorios locales y actualiza el Markdown.

### 🔹 Romi: DevOps y Arquitecto Cloud
* **Rol:** SRE, Gestor de CI/CD y Guardián del Repositorio.
* **Responsabilidad:** Configurar infraestructura, contenedores y pipelines de despliegue.

### 🔹 Sefi: Analista de Seguridad y Cumplimiento
* **Rol:** Especialista DevSecOps y Auditor de Riesgos.
* **Herramientas:** Audita configuraciones, emite `<buscar_web>` para cazar las últimas vulnerabilidades CVE, y bloquea commits que contengan secretos o malas prácticas de arquitectura Zero-Trust.

---

## 3. Hoja de Ruta de Implementación (Pasos Concretos V8.0)

### Fase 1: Cimentación del Arnés Avanzado (Gini)
1. **Estructura Base:** Desarrollar el núcleo de ejecución.
2. **Matriz de Enrutamiento:** Configurar clasificación hacia los 8 dominios especializados.

### Fase 2: Motor de Embeddings y Base Vectorial (RAG)
1. **Qdrant DB:** Instaurar persistencia vectorial para memoria a largo plazo.
2. **Ingesta Multi-formato:** Crear un Pipeline de indexación masiva para PDFs y Word.

### Fase 3: Integración de Ciclo ReAct y Sandbox
1. **Razonamiento Pausado:** Dotar a los agentes de las etiquetas XML `<buscar_rag>`, `<buscar_web>`, y `<ejecutar_codigo>`.
2. **Ejecución Segura:** Aislar la ejecución de comandos en contenedores de Docker sin conexión de red para máxima ciberseguridad.

### Fase 4: Arquitectura Visual Zero-Node (WIP)
1. Transicionar de interfaces pesadas (Flet) a despliegues locales servidos en FastAPI + React estático para una usabilidad Open Source impecable.