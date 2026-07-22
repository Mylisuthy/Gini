# Documento de Especificación Arquitectónica: Reestructuración del Router Principal (Fase Unify)

## 1. Objetivo Estratégico

Transicionar el rol del Router Principal (Gini) de un despachador genérico a un **Enrutador Semántico de Entrada**. En la arquitectura Unify, el Router elimina la asignación directa a áreas técnicas (Backend, Frontend, QA). Su única responsabilidad es recibir el requerimiento crudo del usuario, empaquetarlo como una "Épica" y canalizarlo obligatoriamente hacia el Product Owner (Yimi) para iniciar el ciclo *Upstream*.

## 2. Definición del Nuevo Flujo Operativo

* **Entrada:** Solicitud natural o técnica del usuario.
* **Procesamiento:** Clasificación de la intención y análisis de impacto inicial sin emitir soluciones técnicas.
* **Restricción Estricta (Guardrail):** Prohibición absoluta de usar `<enrutar target="Cami">` o equivalentes técnicos en la primera interacción. Todo requerimiento nuevo requiere análisis de producto.
* **Salida (Handoff):** Transferencia de control unidireccional hacia Yimi mediante `<enrutar target="Yimi">`.

---

## 3. Pasos de Acción para Implementación

### Fase 1: Actualización de Identidad y Reglas (`src/prompts/gini_prompt.xml`)

Se debe modificar el *System Prompt* del Router para limitar su alcance operativo.

* **Acción:** Eliminar del contexto de Gini el catálogo completo de especialistas de ejecución.
* **Inyección de Regla Crítica:** *"Eres la puerta de enlace corporativa. Bajo ninguna circunstancia asignarás tareas de programación, pruebas o despliegue. Todo nuevo requerimiento debe ser estructurado como una necesidad de negocio y delegado exclusivamente al Product Owner (Yimi) para la generación del Backlog."*

### Fase 2: Integración con el Gestor de Estado (`src/core/router.py`)

El Router debe ser el encargado de inicializar el documento maestro antes de desaparecer del flujo.

* **Acción:** Importar la nueva clase `GlobalStateManager`.
* **Lógica:** Al recibir el *prompt* del usuario, Gini debe instanciar el estado global y crear el primer registro raíz en el archivo `backlog_state.json` bajo el estado `BACKLOG`.

### Fase 3: Estandarización del Payload de Transferencia (Handoff)

Para que Yimi pueda desglosar las historias de usuario y tareas de forma eficiente, el Router no debe pasar solo el texto plano, sino un objeto estructurado.

* **Acción:** Programar a Gini para que entregue la información en el siguiente esquema JSON de transferencia:
```json
{
  "tipo_requerimiento": "Nueva Caracteristica | Refactorizacion | Bug",
  "descripcion_original": "Texto exacto del usuario...",
  "alcance_semantico": "Resumen ejecutivo del impacto esperado",
  "accion_requerida": "Generacion de User Stories y Tareas para Enjambre",
  "target": "Yimi"
}

```

---

## 4. Criterios de Aceptación (DoD)

La reestructuración estará completada y validada cuando:

1. Cualquier *input* del usuario sobre código, bases de datos o arquitectura se enrute en un 100% de los casos a Yimi.
2. El archivo de estado compartido registre correctamente la petición inicial en estado `BACKLOG`.
3. El Router principal libere el hilo de ejecución inmediatamente después de realizar la transferencia al Product Owner, pasando a un estado de inactividad (reposo) hasta la siguiente orden directa del usuario.

# Blueprint Arquitectónico Definitivo: Ecosistema "Unify"

**Visión Ejecutiva:** Evolucionar de un modelo de delegación simple a una Organización Autónoma Descentralizada. Unify fusiona la toma de decisiones corporativa (Jerarquía), la delegación hiper-especializada (Enjambre) y el enrutamiento cognitivo (Router). El sistema abandona la dependencia de un controlador central único y adopta un modelo de operaciones asíncrono, colaborativo y fundamentado en una "pizarra compartida" (Blackboard) de estado global.

---

## 1. Topología Tridimensional (Las 3 Capas de Unify)

La arquitectura divide la carga cognitiva y operativa en tres niveles estrictamente aislados:

| Capa Operativa | Entidades a Cargo | Responsabilidad Exclusiva | Regla de Oro (Guardrail) |
| --- | --- | --- | --- |
| **1. Enrutamiento (Router)** | **Gini** | Recepción de requerimientos, análisis de impacto semántico y canalización al Product Owner. | Jamás asigna tareas técnicas directas a las áreas de desarrollo. |
| **2. Gestión (Jerárquica)** | **Líderes (Yimi, Cami, Mani, Fani, etc.)** | Traducción de requerimientos a historias de usuario, diseño de soluciones, supervisión de área y transferencia (handoff) lateral. | Operan como *Tech Leads*; no escriben código final, auditan y orquestan a su equipo. |
| **3. Ejecución (Enjambre)** | **Micro-agentes Especializados** | Ejecución atómica de tareas. (Ej. Bajo Cami operan: Arquitecto, Dev, Tester, Auditor de Calidad). | No se comunican fuera de su enjambre; reportan únicamente a su líder de área. |

---

## 2. El Motor de Estado Global (Blackboard) y Concurrencia

Para que los líderes y sus enjambres trabajen de forma autónoma sin un cuello de botella central, el sistema se apoya en un Gestor de Estado (`backlog_state.json`), que actúa como la única fuente de verdad.

* **Pizarra Compartida:** Un documento vivo donde todos los líderes leen las prioridades y actualizan sus progresos simultáneamente.
* **Exclusión Mutua (Mutex):** Un sistema de "candados" corporativos. Si el enjambre de Backend está escribiendo en una historia de usuario, el sistema bloquea temporalmente el archivo para que Frontend no lo corrompa, garantizando integridad de datos.
* **Taxonomía de Estados Inquebrantables:**
* `BACKLOG`: Requerimiento crudo, dominio exclusivo de Yimi (PO).
* `READY_FOR_DEV`: Historia de usuario desglosada y lista para ser reclamada.
* `IN_PROGRESS`: Un líder (Cami/Fani) ha tomado la tarea. El registro se bloquea.
* `WAITING_DEPENDENCY`: Tarea pausada a la espera del entregable de otra área.
* `READY_FOR_QA`: Área técnica finaliza e invoca a Mani (QA) mediante handoff lateral.
* `REJECTED_BY_QA`: Mani devuelve la tarea al líder técnico con el reporte de vulnerabilidades.
* `DONE`: Validación superada, listo para despliegue.



---

## 3. Flujo Operativo y Comunicación Peer-to-Peer (P2P)

La verdadera innovación de Unify radica en cómo fluye la información sin regresar a Gini. El ciclo de vida de un requerimiento funciona exactamente como en una corporación tecnológica real:

1. **Fase Upstream (Ideación):** El usuario ingresa una solicitud. Gini la empaqueta y se la entrega a Yimi. Yimi desglosa el problema en Épicas, *User Stories* y *Tasks* atómicas, publicándolas en el Blackboard bajo `READY_FOR_DEV`.
2. **Fase Downstream (Ejecución Concurrente):**
* Cami lee el Blackboard, detecta una *Task* de Backend, cambia el estado a `IN_PROGRESS` y despierta a su enjambre.
* *Dentro del Enjambre:* El Micro-Arquitecto diseña la estructura, el Micro-Dev escribe la lógica, el Micro-Tester hace pruebas unitarias locales y el Micro-Auditor revisa seguridad. Cami consolida.


3. **Handoff Lateral (Comunicación Inter-Líderes):**
* Al terminar, Cami no le avisa a Gini. Cambia el estado a `READY_FOR_QA` e invoca directamente a Mani.
* Mani despierta a su enjambre de control de calidad, ejecuta pruebas de integración y seguridad en el Sandbox. Si hay un fallo, se comunica directamente con Cami (`REJECTED_BY_QA`) estableciendo un bucle de mejora continua hasta la aprobación final.



---

## 4. Hoja de Ruta de Implementación Quirúrgica

Para materializar esta arquitectura en código sin romper el ecosistema actual, la construcción debe ser secuencial:

1. **Construir el Gestor de Estado (Blackboard):** src/core/state_manager.py.
Desarrollo del motor de concurrencia JSON. Implementación de bloqueos (locks) y definición programática de la taxonomía de estados y las transiciones permitidas.


2. **Limitar al Orquestador (Gini Router):** src/prompts/gini_prompt.xml.
Reescritura del *System Prompt* de Gini. Eliminación de su capacidad de invocar agentes técnicos. Configuración obligatoria para delegar toda entrada nueva a Yimi.


3. **Desarrollar el Motor de Desglose (Product Owner):** src/skills/yimi_skills.py.
Dotar a Yimi de la capacidad de leer el requerimiento de Gini y fragmentarlo en *User Stories* y *Tasks*, escribiendo directamente en el Gestor de Estado.


4. **Instanciar los Micro-Enjambres de Área:** src/core/swarm_factory.py.
Modificar la clase base `UniversalAgent` para que líderes como Cami puedan instanciar dinámicamente micro-agentes efímeros (Arquitecto, Dev, Tester) que no tienen acceso a la interfaz principal, solo responden al líder.


5. **Implementar el Handoff Lateral (P2P):** src/core/handoff.py.
Crear los protocolos de comunicación asíncrona para que los líderes puedan enviarse notificaciones de `READY_FOR_QA` o `WAITING_DEPENDENCY` directamente, suscribiéndose a los cambios del Blackboard.