document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation ---
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            navItems.forEach(nav => nav.classList.remove('active'));
            viewSections.forEach(view => view.classList.remove('active'));
            
            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');

            if(targetId === 'blackboard-view') {
                loadBlackboard();
            }
        });
    });

    // --- Chat Logic ---
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-msg' : 'system-msg'}`;
        msgDiv.innerHTML = `<div class="msg-bubble">${text}</div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, true);
        chatInput.value = '';
        chatInput.disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            
            addMessage(data.message || 'Solicitud procesada.');
        } catch (error) {
            addMessage('Error de conexión con el backend.');
        } finally {
            chatInput.disabled = false;
            chatInput.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // --- Blackboard Logic ---
    const refreshBtn = document.getElementById('refresh-board');
    refreshBtn.addEventListener('click', loadBlackboard);

    function getColumnIdForState(state) {
        if (state === 'BACKLOG') return 'col-backlog';
        if (state === 'READY_FOR_DEV') return 'col-ready';
        if (state === 'IN_PROGRESS') return 'col-progress';
        if (state === 'READY_FOR_QA' || state === 'REJECTED_BY_QA') return 'col-qa';
        if (state === 'DONE') return 'col-done';
        return 'col-backlog';
    }

    async function loadBlackboard() {
        try {
            // Limpiar columnas
            document.querySelectorAll('.cards-container').forEach(c => c.innerHTML = '');

            const response = await fetch('/api/blackboard');
            const data = await response.json();

            const epics = data.backlog_activo || [];
            epics.forEach(epic => {
                const colId = getColumnIdForState(epic.estado_actual);
                const container = document.querySelector(`#${colId} .cards-container`);
                if (container) {
                    const card = document.createElement('div');
                    card.className = 'epic-card';
                    
                    let title = "Requerimiento en Análisis";
                    if (epic.detalles && epic.detalles.tipo_requerimiento) {
                        title = epic.detalles.tipo_requerimiento;
                    }
                    if (epic.desglose && epic.desglose.iniciativa && epic.desglose.iniciativa.titulo) {
                        title = epic.desglose.iniciativa.titulo;
                    }

                    const date = epic.fecha_actualizacion ? new Date(epic.fecha_actualizacion).toLocaleTimeString() : new Date(epic.timestamp).toLocaleTimeString();

                    card.innerHTML = `
                        <div class="epic-id">${epic.id}</div>
                        <div class="epic-title">${title}</div>
                        <div class="epic-meta">
                            <span>Estado: ${epic.estado_actual}</span>
                            <span>${date}</span>
                        </div>
                    `;

                    card.addEventListener('click', () => showDetails(epic));
                    container.appendChild(card);
                }
            });
        } catch (error) {
            console.error("Error cargando blackboard", error);
        }
    }

    // --- Modal Logic ---
    const modal = document.getElementById('details-modal');
    const closeBtn = document.querySelector('.close-btn');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    function showDetails(epic) {
        modalTitle.textContent = `Detalles del Epic: ${epic.id}`;
        let detailsHtml = `<strong>Estado Actual:</strong> ${epic.estado_actual}<br><br>`;
        
        if (epic.desglose) {
            detailsHtml += `<pre>${JSON.stringify(epic.desglose, null, 2)}</pre>`;
        } else if (epic.detalles) {
            detailsHtml += `<pre>${JSON.stringify(epic.detalles, null, 2)}</pre>`;
        }
        
        modalBody.innerHTML = detailsHtml;
        modal.classList.add('show');
    }

    closeBtn.addEventListener('click', () => modal.classList.remove('show'));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('show');
    });

    // Auto-load on init
    loadBlackboard();
    // Auto-poll every 5 seconds for live feel
    setInterval(loadBlackboard, 5000);
});
