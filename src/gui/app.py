import sys
import os
import json
import threading

# Parche crítico para resolver el módulo 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft
from src.core import router, evo_agent
from src.core.universal_agent import UniversalAgent
from src.core.config_manager import config

COLORS = {
    "gini": "#c026d3", "yimi": "#3b82f6", "tobi": "#6366f1", "fani": "#ec4899",
    "romi": "#8b5cf6", "mani": "#ef4444", "cami": "#10b981", "evo": "#f97316",
    "sefi": "#06b6d4", "user": "#4f46e5", "bg_main": "#0B0F19", "bg_panel": "#111827",
    "border": "#1e293b", "text_muted": "#64748b"
}

ICONS = {
    "gini": "share", "yimi": "dashboard", "tobi": "android",
    "fani": "brush", "romi": "security", "mani": "bug_report",
    "cami": "terminal", "evo": "science", "sefi": "storage", "usuario": "person"
}

def premium_button(text, bg_color, hover_color, on_click, icon=None):
    content_row = [ft.Icon(icon, size=16), ft.Text(text, size=13, weight=ft.FontWeight.W_500)] if icon else [ft.Text(text, size=13, weight=ft.FontWeight.W_500)]
    return ft.Container(
        content=ft.Row(content_row, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=bg_color,
        border_radius=6,
        padding=ft.Padding(left=15, top=12, right=15, bottom=12),
        on_click=on_click
    )

def main(page: ft.Page):
    page.title = "Gini V8.0 | Swarm Orchestrator"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = COLORS["bg_main"]
    
    gini_router = router.GiniRouter()
    evo = evo_agent.EvoAgent()

    # ==========================
    # TELEMETRÍA (Panel Derecho)
    # ==========================
    telemetry_list = ft.ListView(expand=True, spacing=10, padding=15)
    telemetry_agents = {}
    
    def init_telemetry():
        agents_data = [
            ("Gini", "Router Principal", "gini"), ("Evo", "Arqui. Mutación", "evo"),
            ("Yimi", "Product Owner", "yimi"), ("Fani", "Frontend Dev", "fani"),
            ("Cami", "Backend Dev", "cami"), ("Mani", "QA Automation", "mani"),
            ("Romi", "DevSecOps", "romi"), ("Sefi", "Data Engineer", "sefi")
        ]
        
        for name, role, key in agents_data:
            status_indicator = ft.Container(width=8, height=8, border_radius=4, bgcolor="#475569")
            status_text = ft.Text("Standby", size=11, color="#64748b", weight=ft.FontWeight.W_500)
            
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Row([status_indicator, ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color="white")]),
                        ft.Container(
                            content=ft.Text(role, size=9, weight=ft.FontWeight.BOLD),
                            bgcolor=f"{COLORS.get(key, '#ffffff')}22",
                            border=ft.Border.all(1, f"{COLORS.get(key, '#ffffff')}55"),
                            padding=ft.Padding(left=6, top=2, right=6, bottom=2),
                            border_radius=4,
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([ft.Icon(ICONS.get(key), size=12, color="#64748b"), status_text], spacing=5)
                ]),
                bgcolor=COLORS["bg_main"], border=ft.Border.all(1, COLORS["border"]), border_radius=8, padding=12
            )
            telemetry_agents[key.lower()] = {"indicator": status_indicator, "text": status_text, "card": card}
            telemetry_list.controls.append(card)

    def update_telemetry(agent_key, status):
        key = agent_key.lower()
        if key not in telemetry_agents: return
        t = telemetry_agents[key]
        
        states = {
            "processing": ("#10b981", "Sintetizando..."),
            "working": ("#3b82f6", "Ejecutando hilos..."),
            "error": ("#ef4444", "Fallo cognitivo"),
            "completed": ("#6366f1", "Tarea finalizada"),
            "idle": ("#475569", "Standby")
        }
        color, text = states.get(status, states["idle"])
        t["indicator"].bgcolor = color
        t["text"].value = text
        t["text"].color = color
        page.update()

    init_telemetry()
    
    right_panel = ft.Container(
        width=280, bgcolor=COLORS["bg_panel"], border=ft.Border.only(left=ft.BorderSide(1, COLORS["border"])),
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Row([ft.Icon("activity", size=16, color="#6366f1"), ft.Text("Telemetría del Enjambre", size=13, weight=ft.FontWeight.BOLD, color="white")]),
                    ft.Container(width=8, height=8, border_radius=4, bgcolor="#10b981")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=20, border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            ),
            telemetry_list
        ], spacing=0)
    )

    # ==========================
    # PANEL IZQUIERDO (Nav)
    # ==========================
    left_panel = ft.Container(
        width=260, bgcolor=COLORS["bg_panel"], border=ft.Border.only(right=ft.BorderSide(1, COLORS["border"])),
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Icon("activity", size=20, color="#818cf8"), bgcolor="#4f46e533", border=ft.Border.all(1, "#4f46e544"), border_radius=8, width=32, height=32, alignment=ft.Alignment.CENTER),
                    ft.Text("Gini", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("V8.0", size=18, weight=ft.FontWeight.W_300, color="#818cf8")
                ]), padding=20, border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            ),
            ft.Container(
                content=ft.Container(
                    content=ft.Row([ft.Icon("add", size=16, color="white"), ft.Text("Nuevo Hilo Operativo", size=13, weight=ft.FontWeight.W_500, color="white")], alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor="#4f46e5", border_radius=6, padding=15,
                    on_click=lambda e: chat_list.controls.clear() or page.update()
                ), padding=15
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("SESIONES ACTIVAS", size=10, weight=ft.FontWeight.BOLD, color="#64748b"),
                    ft.Container(content=ft.Row([ft.Icon("tag", size=14, color="#818cf8"), ft.Text("Simulación Principal", size=13, color="#c7d2fe")]), bgcolor="#1e293b", padding=12, border_radius=6, border=ft.Border.all(1, "#334155"))
                ]), padding=ft.Padding(left=15, top=0, right=15, bottom=0)
            ),
            ft.Container(
                content=ft.Row([ft.Icon("settings", size=16, color="#94a3b8"), ft.Text("Ajustes del Enjambre", size=13, color="#94a3b8")]),
                padding=20, bgcolor="#0B0F1988", border=ft.Border.only(top=ft.BorderSide(1, COLORS["border"]))
            )
        ], spacing=0)
    )

    # ==========================
    # ÁREA CENTRAL (Vistas)
    # ==========================
    chat_list = ft.ListView(expand=True, spacing=25, auto_scroll=True, padding=30)
    evo_list = ft.ListView(expand=True, spacing=25, auto_scroll=True, padding=30, visible=False)
    
    # --- Vista: Configuración (Seguridad) ---
    gemini_key_input = ft.TextField(label="GEMINI_API_KEY", value=config.get("GEMINI_API_KEY"), password=True, can_reveal_password=True, border_radius=8, border_color=COLORS["border"], bgcolor="#090c15")
    azure_org_input = ft.TextField(label="AZURE_DEVOPS_ORG", value=config.get("AZURE_DEVOPS_ORG"), border_radius=8, border_color=COLORS["border"], bgcolor="#090c15")
    azure_pat_input = ft.TextField(label="AZURE_DEVOPS_PAT", value=config.get("AZURE_DEVOPS_PAT"), password=True, can_reveal_password=True, border_radius=8, border_color=COLORS["border"], bgcolor="#090c15")
    
    def save_settings(e):
        config.set("GEMINI_API_KEY", gemini_key_input.value)
        config.set("AZURE_DEVOPS_ORG", azure_org_input.value)
        config.set("AZURE_DEVOPS_PAT", azure_pat_input.value)
        page.overlay.append(ft.SnackBar(ft.Text("✅ Configuración cifrada guardada exitosamente."), bgcolor="#10b981", open=True))
        page.update()

    config_view = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon("security", color="#10b981", size=30), ft.Text("Bóveda de Credenciales (Zero Trust)", size=24, weight=ft.FontWeight.BOLD, color="white")]),
            ft.Text("Tus tokens son encriptados con Fernet (Criptografía Simétrica) y guardados localmente.", color="#64748b"),
            ft.Divider(color=COLORS["border"], height=30),
            gemini_key_input, azure_org_input, azure_pat_input,
            ft.Container(height=10),
            premium_button("Guardar Configuración Cifrada", "#059669", "#10b981", save_settings, icon="shield")
        ], spacing=15), padding=40, expand=True, visible=False
    )

    # --- Renderizado de Mensajes ---
    def add_user_message(target_list, text):
        msg = ft.Row([
            ft.Container(content=ft.Text(text, size=14, color="white", weight=ft.FontWeight.W_500), bgcolor=COLORS["user"], padding=15, border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15, bottom_right=5), border=ft.Border.all(1, "#4338ca"))
        ], alignment=ft.MainAxisAlignment.END)
        target_list.controls.append(msg)
        page.update()

    def add_agent_message(target_list, agent_key, role, text):
        c = COLORS.get(agent_key.lower(), COLORS["yimi"])
        msg = ft.Row([
            ft.Container(content=ft.Icon(ICONS.get(agent_key, "person"), size=20, color=c), width=40, height=40, border_radius=8, bgcolor=f"{c}22", border=ft.Border.all(1, f"{c}55"), alignment=ft.Alignment.CENTER),
            ft.Column([
                ft.Text(f"{agent_key.upper()} | {role.upper()}", size=10, weight=ft.FontWeight.BOLD, color=c),
                ft.Container(content=ft.Markdown(text, selectable=True, extension_set="gitHubWeb"), bgcolor="#0f172a", padding=12, border_radius=8, border=ft.Border(top=ft.BorderSide(1, COLORS["border"]), right=ft.BorderSide(1, COLORS["border"]), bottom=ft.BorderSide(1, COLORS["border"]), left=ft.BorderSide(3, c)))
            ], spacing=4)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
        target_list.controls.append(msg)
        page.update()

    def add_evo_alert(text):
        alert = ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Icon("warning", size=24, color="#f97316"), width=48, height=48, border_radius=24, bgcolor="#f9731633", border=ft.Border.all(1, "#f9731655"), alignment=ft.Alignment.CENTER),
                ft.Column([
                    ft.Row([
                        ft.Text("ALERTA DE AUTO-EVOLUCIÓN", size=14, weight=ft.FontWeight.BOLD, color="#f97316"),
                        ft.Container(content=ft.Text("Requiere Acción", size=9, color="#fb923c"), bgcolor="#f9731633", padding=ft.Padding(left=8, top=2, right=8, bottom=2), border_radius=10, border=ft.Border.all(1, "#f9731655"))
                    ]),
                    ft.Text(text, size=13, color="#fed7aa", width=600),
                    ft.Row([
                        premium_button("Autorizar Mutación (Invocar EVO)", "#ea580c", "#f97316", lambda e: add_agent_message(chat_list, "Evo", "Laboratorio", "Mutación autorizada. Ejecutando protocolo XML en segundo plano..."), icon="science"),
                        ft.Container(content=ft.Text("Ignorar y Continuar", color="#fdba74", size=12), bgcolor="transparent", border_radius=6, padding=10)
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=8)
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor="#431407aa", border=ft.Border.all(1, "#ea580c55"), padding=20, border_radius=12, margin=ft.Margin.symmetric(vertical=20)
        )
        chat_list.controls.append(alert)
        page.update()

    def create_action_card(agent_name, agent_instance, plan_data, user_text):
        c = COLORS.get(agent_name.lower(), COLORS["yimi"])
        
        reflection_ui = ft.Container()
        if "reflexion" in plan_data:
            reflection_ui = ft.Container(
                content=ft.Row([
                    ft.Icon("warning_amber_rounded", color="#f59e0b", size=20),
                    ft.Column([
                        ft.Text("AUTO-REFLEXIÓN DEL AGENTE", size=10, weight=ft.FontWeight.BOLD, color="#f59e0b"),
                        ft.Text(plan_data["reflexion"], size=13, color="#fde68a")
                    ], spacing=2, expand=True)
                ], vertical_alignment=ft.CrossAxisAlignment.START),
                bgcolor="#f59e0b11", padding=15, border=ft.Border.only(bottom=ft.BorderSide(1, "#f59e0b33"))
            )
            
        strategy_ui = ft.Container(
            content=ft.Column([
                ft.Text("ESTRATEGIA", size=10, weight=ft.FontWeight.BOLD, color="#64748b"),
                ft.Markdown(plan_data.get("explicacion", "Sin estrategia definida."), selectable=True, extension_set="gitHubWeb")
            ], spacing=5), padding=15, border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
        )
        
        files_ui = ft.Column(spacing=0)
        for f in plan_data.get("archivos", []):
            content = f.get('contenido', '')
            if '```' in content: content = content.replace('```python\n','').replace('```html\n','').replace('```\n','').replace('```','')
            files_ui.controls.append(ft.Container(
                content=ft.Column([
                    ft.Text(f"// {f.get('nombre')}", size=11, color="#64748b", font_family="monospace"),
                    ft.Text(content, size=12, color="#6ee7b7", font_family="monospace", selectable=True)
                ], spacing=10), bgcolor="#090c15", padding=15, border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            ))

        comandos = plan_data.get("comandos", [])
        if comandos:
            files_ui.controls.append(ft.Container(
                content=ft.Column([
                    ft.Text("// Comandos de terminal", size=11, color="#64748b", font_family="monospace"),
                    ft.Text("\n".join(comandos), size=12, color="#6ee7b7", font_family="monospace", selectable=True)
                ], spacing=10), bgcolor="#090c15", padding=15, border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            ))

        terminal_area = ft.Container(visible=False, bgcolor="#05080f", padding=15, border=ft.Border.only(top=ft.BorderSide(1, COLORS["border"])))
        terminal_col = ft.Column(spacing=5)
        terminal_area.content = terminal_col
        
        controls_area = ft.Container(bgcolor="#312e8122", padding=15, border=ft.Border.only(top=ft.BorderSide(1, "#4f46e533")))
        
        def run_execution():
            terminal_col.controls.clear()
            terminal_col.controls.append(ft.Row([ft.Icon("terminal", size=14, color="#64748b"), ft.Text("root@gini-v8:~# Inyectando en local...", size=11, color="#64748b", font_family="monospace")]))
            terminal_area.visible = True
            controls_area.visible = False
            status_text.value = "EN PRODUCCIÓN"
            status_text.color = "#818cf8"
            status_container.bgcolor = "#4f46e522"
            status_container.border = ft.Border.all(1, "#4f46e555")
            update_telemetry(agent_name, "working")
            page.update()
            
            try:
                res = agent_instance.execute_plan(plan_data, user_text)
                terminal_col.controls.append(ft.Text(f"> [EXITO] Despliegue completado.\n{res}", size=12, color="#34d399", font_family="monospace"))
                update_telemetry(agent_name, "completed")
            except Exception as ex:
                terminal_col.controls.append(ft.Text(f"> [ERROR] Falló la inyección.\n{str(ex)}", size=12, color="#ef4444", font_family="monospace"))
                update_telemetry(agent_name, "error")
            page.update()

        btn_approve = premium_button("Aprobar e Inyectar", "#059669", "#10b981", lambda e: threading.Thread(target=run_execution, daemon=True).start(), icon="play_circle_fill")
        btn_reject = ft.Container(
            content=ft.Row([ft.Icon("close", size=16, color="#f87171"), ft.Text("Rechazar", size=13, color="#f87171")]),
            bgcolor="#7f1d1d33", border_radius=6, padding=10,
            on_click=lambda e: [setattr(controls_area, 'visible', False), setattr(terminal_area, 'visible', True), terminal_col.controls.append(ft.Text("> [CANCELADO] Operación abortada por el usuario.", size=12, color="#ef4444", font_family="monospace")), update_telemetry(agent_name, "idle"), page.update()]
        )
        
        controls_area.content = ft.Row([
            ft.Row([ft.Icon("hourglass_empty", size=14, color="#818cf8"), ft.Text("Esperando autorización humana...", size=12, color="#818cf8")]),
            ft.Row([btn_reject, btn_approve])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        status_text = ft.Text("SINTETIZANDO...", size=9, weight=ft.FontWeight.BOLD, color="#34d399")
        status_container = ft.Container(
            content=ft.Row([ft.Icon("autorenew", size=12, color="#34d399"), status_text]),
            bgcolor="#10b98122", border=ft.Border.all(1, "#10b98155"), padding=ft.Padding(left=8, top=2, right=8, bottom=2), border_radius=10
        )

        agent_header = ft.Row([
            ft.Container(content=ft.Icon(ICONS.get(agent_name.lower(), "person"), size=20, color=c), width=40, height=40, border_radius=8, bgcolor=f"{c}22", border=ft.Border.all(1, f"{c}55"), alignment=ft.Alignment.CENTER),
            ft.Column([
                ft.Row([ft.Text(f"{agent_name.upper()} | ESPECIALISTA", size=10, weight=ft.FontWeight.BOLD, color=c), status_container])
            ], spacing=4)
        ], vertical_alignment=ft.CrossAxisAlignment.START)

        card_body = ft.Container(
            content=ft.Column([reflection_ui, strategy_ui, files_ui, controls_area, terminal_area], spacing=0),
            bgcolor=COLORS["bg_panel"], border=ft.Border.all(1, COLORS["border"]), border_radius=12, margin=ft.Margin.only(left=55), clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        chat_list.controls.append(ft.Column([agent_header, card_body], spacing=10))
        update_telemetry(agent_name, "processing")
        page.update()
        
        status_text.value = "ESPERANDO APROBACIÓN"
        status_text.color = "#818cf8"
        status_container.bgcolor = "#4f46e522"
        status_container.border = ft.Border.all(1, "#4f46e555")
        update_telemetry(agent_name, "waiting")
        page.update()

    # --- Lógica de Input (Chat Central) ---
    def process_chat_input(e):
        text = user_input.value
        if not text: return
        user_input.value = ""
        user_input.disabled = True
        send_btn.disabled = True
        add_user_message(chat_list, text)
        
        spinner = ft.Row([ft.ProgressRing(width=16, height=16, color=COLORS["gini"], stroke_width=2), ft.Text("Gini analizando arquitectura...", color=COLORS["gini"], italic=True, size=12)])
        chat_list.controls.append(spinner)
        update_telemetry("gini", "processing")
        page.update()
        
        def run_ai():
            decision = gini_router.analyze_intent(text)
            chat_list.controls.remove(spinner)
            update_telemetry("gini", "idle")
            
            if decision.get("action") == "respond":
                add_agent_message(chat_list, "Gini", "Router Principal", decision.get("message", ""))
            elif decision.get("action") == "route_multiple":
                targets = decision.get("targets", [])
                msg_text = "Analizando requerimiento arquitectónico. Dividiendo la tarea en hilos paralelos:\n"
                for t in targets: msg_text += f"- Asignando tareas a **@{t['agent'].upper()}**\n"
                msg_text += "Iniciando orquestación..."
                add_agent_message(chat_list, "Gini", "Router Principal", msg_text)
                
                for t in targets:
                    target_name = t["agent"]
                    def run_agent_task(name, p_text):
                        update_telemetry(name, "processing")
                        try:
                            agent_instance = UniversalAgent(name)
                            plan = agent_instance.generate_plan(p_text)
                            if "error" in plan:
                                update_telemetry(name, "error")
                                add_agent_message(chat_list, name, "Especialista", f"Error interno: {plan['error']}")
                            else:
                                if plan.get("auto_evolucion"):
                                    add_evo_alert(plan["auto_evolucion"].get("motivo", "Fallo cognitivo detectado. Requiere mutación de cerebro XML."))
                                create_action_card(name, agent_instance, plan, p_text)
                        except Exception as ex:
                            update_telemetry(name, "error")
                            add_agent_message(chat_list, "Sistema", "Error Crítico", f"Especialista {name} falló críticamente: {str(ex)}")
                        page.update()
                    threading.Thread(target=run_agent_task, args=(target_name, text), daemon=True).start()
    
            user_input.disabled = False
            send_btn.disabled = False
            page.update()
            
        threading.Thread(target=run_ai, daemon=True).start()

    # --- Lógica de Input (Evo) ---
    def process_evo_input(e):
        text = user_input.value
        if not text: return
        user_input.value = ""
        user_input.disabled = True
        send_btn.disabled = True
        add_user_message(evo_list, text)
        
        spinner = ft.Row([ft.ProgressRing(width=16, height=16, color=COLORS["evo"], stroke_width=2), ft.Text("Evo analizando matriz...", color=COLORS["evo"], italic=True, size=12)])
        evo_list.controls.append(spinner)
        update_telemetry("evo", "processing")
        page.update()
        
        def run_evo():
            decision = evo.analyze_request(text)
            evo_list.controls.remove(spinner)
            update_telemetry("evo", "idle")
            
            if decision.get("action") == "respond":
                add_agent_message(evo_list, "Evo", "Arquitecto", decision.get("message", ""))
            elif decision.get("action") == "update_agent":
                a_name = decision.get("agent_name")
                p_content = decision.get("prompt_content")
                add_agent_message(evo_list, "Evo", "Arquitecto", f"He preparado la matriz para **{a_name}**. ¿Deseas inyectarla?\n\n```xml\n{p_content}\n```")
            # Soporte completo de Evo se añadiría como tarjetas igual que en chat_list
            user_input.disabled = False
            send_btn.disabled = False
            page.update()
            
        threading.Thread(target=run_evo, daemon=True).start()

    # Shared Input Area
    user_input = ft.TextField(
        hint_text="Ingresa un requerimiento...", expand=True, border_color=ft.Colors.TRANSPARENT, bgcolor=ft.Colors.TRANSPARENT,
        color="white", multiline=True, min_lines=1, max_lines=4, hint_style=ft.TextStyle(color="#475569")
    )
    send_btn = ft.IconButton(
        icon="send", icon_color="white", bgcolor="#4f46e5", icon_size=18,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=12),
        on_click=process_chat_input # Will be swapped dynamically
    )
    input_container = ft.Container(
        content=ft.Row([ft.Icon("terminal", color="#64748b", size=20), user_input, send_btn], alignment=ft.MainAxisAlignment.START),
        bgcolor=COLORS["bg_main"], border=ft.Border.all(1, COLORS["border"]), border_radius=12, padding=ft.Padding.only(left=15, right=10, top=5, bottom=5)
    )

    # --- TABS y Rutas ---
    def switch_tab(tab_name):
        # Reset styles
        tab_chat.border = None
        tab_chat.content.controls[1].color = "#64748b"
        tab_chat.content.controls[0].color = "#64748b"
        
        tab_evo.border = None
        tab_evo.content.controls[1].color = "#64748b"
        tab_evo.content.controls[0].color = "#64748b"
        
        tab_sec.border = None
        tab_sec.content.controls[1].color = "#64748b"
        tab_sec.content.controls[0].color = "#64748b"

        if tab_name == "chat":
            tab_chat.border = ft.Border.only(bottom=ft.BorderSide(2, "#4f46e5"))
            tab_chat.content.controls[1].color = "#818cf8"
            tab_chat.content.controls[0].color = "#818cf8"
            chat_list.visible = True
            evo_list.visible = False
            config_view.visible = False
            send_btn.on_click = process_chat_input
            input_container.visible = True
        elif tab_name == "evo":
            tab_evo.border = ft.Border.only(bottom=ft.BorderSide(2, "#ea580c"))
            tab_evo.content.controls[1].color = "#fb923c"
            tab_evo.content.controls[0].color = "#fb923c"
            chat_list.visible = False
            evo_list.visible = True
            config_view.visible = False
            send_btn.on_click = process_evo_input
            input_container.visible = True
        elif tab_name == "security":
            tab_sec.border = ft.Border.only(bottom=ft.BorderSide(2, "#10b981"))
            tab_sec.content.controls[1].color = "#34d399"
            tab_sec.content.controls[0].color = "#34d399"
            chat_list.visible = False
            evo_list.visible = False
            config_view.visible = True
            input_container.visible = False
            
        page.update()

    tab_chat = ft.Container(content=ft.Row([ft.Icon("terminal", size=16), ft.Text("Panel de Orquestación", size=13, weight=ft.FontWeight.W_500)]), padding=ft.Padding.only(bottom=10), on_click=lambda e: switch_tab("chat"), ink=True)
    tab_evo = ft.Container(content=ft.Row([ft.Icon("science", size=16), ft.Text("Laboratorio Evo", size=13, weight=ft.FontWeight.W_500)]), padding=ft.Padding.only(bottom=10), on_click=lambda e: switch_tab("evo"), ink=True)
    tab_sec = ft.Container(content=ft.Row([ft.Icon("security", size=16), ft.Text("Seguridad (Zero Trust)", size=13, weight=ft.FontWeight.W_500)]), padding=ft.Padding.only(bottom=10), on_click=lambda e: switch_tab("security"), ink=True)
    
    switch_tab("chat") # Init active

    tabs_header = ft.Container(
        content=ft.Row([tab_chat, tab_evo, tab_sec], spacing=25),
        bgcolor=COLORS["bg_panel"], padding=ft.Padding.only(left=30, right=30, top=15), border=ft.Border.only(bottom=ft.BorderSide(1, COLORS["border"]))
    )

    center_panel = ft.Container(
        expand=True, bgcolor=COLORS["bg_main"],
        content=ft.Column([
            tabs_header,
            chat_list, evo_list, config_view,
            ft.Container(
                content=ft.Column([
                    input_container,
                    ft.Row([ft.Container(width=6, height=6, border_radius=3, bgcolor="#10b981"), ft.Text("Gini en línea. Enjambre listo para orquestación paralela.", size=11, color="#64748b", weight=ft.FontWeight.W_500)], alignment=ft.MainAxisAlignment.CENTER)
                ]), bgcolor=COLORS["bg_panel"], border=ft.Border.only(top=ft.BorderSide(1, COLORS["border"])), padding=25
            )
        ], spacing=0)
    )

    # --- Ensamblaje Principal ---
    def handle_resize(e):
        h = page.window_height if hasattr(page, "window_height") else page.height
        if h:
            left_panel.height = h
            center_panel.height = h
            right_panel.height = h
            page.update()
            
    page.on_resized = handle_resize
    
    # Asignación inicial segura
    h = page.window_height if hasattr(page, "window_height") else page.height
    if h and h > 0:
        left_panel.height = h
        center_panel.height = h
        right_panel.height = h

    page.add(ft.Row([left_panel, center_panel, right_panel], expand=True, spacing=0))
    add_agent_message(chat_list, "Gini", "Router Principal", "¡Sistema V8.0 en línea! La interfaz visual ha sido actualizada al nuevo diseño de alta fidelidad.")
    add_agent_message(evo_list, "Evo", "Arqui. Mutación", "Laboratorio activado. Puedes probar o mutar agentes desde aquí.")

if __name__ == "__main__":
    ft.app(target=main)
