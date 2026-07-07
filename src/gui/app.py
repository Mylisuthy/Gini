import sys
import os
import json
import asyncio

# Parche crítico para resolver el módulo 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import flet as ft
from src.core import router, evo_agent
from src.core.universal_agent import UniversalAgent
from src.core.config_manager import config

COLORS = {
    "gini": "#EC407A",
    "yimi": "#42A5F5",
    "tobi": "#26C6DA",
    "fani": "#FFEE58",
    "romi": "#EF5350",
    "mani": "#66BB6A",
    "evo": "#AB47BC",
    "user": "#FFFFFF",
    "bg_start": "#0F172A", # Slate 900
    "bg_end": "#020617", # Slate 950
    "glass": "#1AFFFFFF", # Transparencia para Glassmorphism
    "glass_border": "#33FFFFFF"
}

EMOJIS = {
    "gini": "🧠", "yimi": "📋", "tobi": "🤖", "fani": "🎨", "romi": "⚙️", "mani": "🛡️", "evo": "🧬", "usuario": "👤"
}

def create_glass_container(content_ui, border_color=COLORS["glass_border"], padding=15, expand=False):
    return ft.Container(
        content=content_ui,
        padding=padding,
        border_radius=15,
        bgcolor=COLORS["glass"],
        blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR),
        border=ft.Border.all(1, border_color),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="#40000000", offset=ft.Offset(0, 5)),
        expand=expand
    )

def premium_button(text, base_color, hover_color, on_click, icon=None):
    return ft.ElevatedButton(
        content=text,
        icon=icon,
        style=ft.ButtonStyle(
            color="white",
            bgcolor={"hovered": hover_color, "": base_color},
            animation_duration=300,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=on_click
    )

def main(page: ft.Page):
    page.title = "Sistema Multi-Agente Corporativo V5.1"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800

    gini_router = router.GiniRouter()
    evo = evo_agent.EvoAgent()
    
    # ==========================================
    # 1. CHAT CENTRAL (Operaciones)
    # ==========================================
    chat_list = ft.ListView(expand=True, spacing=15, auto_scroll=True, padding=20)
    user_input = ft.TextField(
        hint_text="Describe tu tarea de desarrollo...", 
        expand=True, border_color="#1976D2", multiline=True, min_lines=1, max_lines=5,
        border_radius=10, focused_border_color=COLORS["yimi"]
    )
    
    def add_message(target_list, sender, text, role_color, is_markdown=False):
        emoji = EMOJIS.get(sender.lower(), "👽")
        avatar = ft.CircleAvatar(content=ft.Text(emoji, size=20), bgcolor=role_color)
        content_ui = ft.Markdown(text, selectable=True, extension_set="gitHubWeb") if is_markdown else ft.Text(text, selectable=True, color="white")
        row = ft.Row(
            [avatar, create_glass_container(content_ui, border_color=role_color, padding=10, expand=True)],
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        target_list.controls.append(row)
        page.update()

    def create_action_card(agent_name, agent_instance, plan_data, user_text):
        md_text = ""
        if "reflexion" in plan_data:
            md_text += f"> [!NOTE]\n> **Auto-Reflexión ({agent_name.upper()}):**\n> {plan_data['reflexion']}\n\n"
            
        md_text += f"**Estrategia Propuesta:**\n{plan_data.get('explicacion', '')}\n\n"
        
        for file in plan_data.get("archivos", []):
            content = file.get('contenido', '')
            if '```' in content:
                md_text += f"**{file.get('nombre')}**\n\n{content}\n\n"
            else:
                md_text += f"**{file.get('nombre')}**\n```\n{content}\n```\n\n"

        comandos = plan_data.get("comandos", [])
        if comandos:
            md_text += "**Comandos a Ejecutar:**\n```bash\n" + "\n".join(comandos) + "\n```\n"

        if "azure_backlog" in plan_data:
            md_text += f"```json\n{json.dumps(plan_data['azure_backlog'], indent=2)}\n```"

        auto_ev = plan_data.get("auto_evolucion")
        if auto_ev:
            md_text += f"\n\n> [!WARNING]\n> **🧬 PROPUESTA DE AUTO-EVOLUCIÓN**\n> **Motivo:** {auto_ev.get('motivo')}\n> **Nuevos Conocimientos:** {auto_ev.get('nuevos_conocimientos')}\n"

        # Limitamos la altura a 350px para evitar desbordamiento y habilitamos scroll
        card_content = ft.Column(
            [ft.Markdown(md_text, selectable=True, extension_set="gitHubWeb")],
            scroll=ft.ScrollMode.AUTO,
            height=350
        )
        
        def on_approve(e):
            card_content.controls.remove(btn_row)
            loading_row = ft.Row([ft.ProgressRing(width=20, height=20, color="green"), ft.Text("✅ Aceptado. Ejecutando operación...", color="green")])
            card_content.controls.append(loading_row)
            page.update()
            
            def run_task():
                try:
                    res = agent_instance.execute_plan(plan_data, user_text)
                    card_content.controls.remove(loading_row)
                    card_content.controls.append(ft.Text(f"✅ Éxito:\n{res}", color="#66BB6A"))
                except Exception as ex:
                    card_content.controls.remove(loading_row)
                    card_content.controls.append(ft.Text(f"❌ Error:\n{str(ex)}", color="#EF5350"))
                page.update()
            import threading
            threading.Thread(target=run_task, daemon=True).start()

        def on_reject(e):
            card_content.controls.remove(btn_row)
            card_content.controls.append(ft.Text("🛑 Operación Cancelada", color="#EF5350"))
            page.update()

        btn_approve = premium_button("Aprobar y Ejecutar", "#2E7D32", "#388E3C", on_approve, icon="check")
        btn_reject = premium_button("Rechazar", "#C62828", "#D32F2F", on_reject, icon="cancel")
        btn_row = ft.Row([btn_approve, btn_reject])
        
        card_content.controls.append(btn_row)
        chat_list.controls.append(create_glass_container(card_content, border_color=COLORS.get(agent_name.lower(), "blue")))
        page.update()

    def process_input(e):
        text = user_input.value
        if not text: return
        
        user_input.value = ""
        user_input.disabled = True
        send_btn.disabled = True
        add_message(chat_list, "Usuario", text, COLORS["user"])
        
        spinner = ft.Row([ft.ProgressRing(width=20, height=20, color=COLORS["gini"]), ft.Text("Gini enrutando tu solicitud...", color=COLORS["gini"], italic=True)])
        chat_list.controls.append(spinner)
        page.update()
        
        def run_ai():
            decision = gini_router.analyze_intent(text)
            chat_list.controls.remove(spinner)
            
            if decision.get("action") == "respond":
                add_message(chat_list, "Gini", decision.get("message", ""), COLORS["gini"])
            elif decision.get("action") == "route_multiple":
                targets = decision.get("targets", [])
                for t in targets:
                    target = t["agent"]
                    msg = t["message"]
                    add_message(chat_list, "Gini", f"Enrutando tarea en paralelo a {target}: {msg}", COLORS["gini"])
                    
                    agent_color = COLORS.get(target.lower(), "#42A5F5")
                    agent_spinner = ft.Row([ft.ProgressRing(width=20, height=20, color=agent_color), ft.Text(f"{target.upper()} procesando código...", color=agent_color, italic=True)])
                    chat_list.controls.append(agent_spinner)
                    
                    def run_agent_task(target_name, spinner_ref):
                        try:
                            agent_instance = UniversalAgent(target_name)
                            plan = agent_instance.generate_plan(text)
                            chat_list.controls.remove(spinner_ref)
                            
                            if "error" in plan:
                                add_message(chat_list, target_name.capitalize(), f"Error interno: {plan['error']}", agent_color)
                            else:
                                create_action_card(target_name, agent_instance, plan, text)
                        except Exception as ex:
                            if spinner_ref in chat_list.controls: chat_list.controls.remove(spinner_ref)
                            add_message(chat_list, "Sistema", f"Especialista {target_name} falló: {str(ex)}", "red")
                        page.update()
                    
                    import threading
                    threading.Thread(target=run_agent_task, args=(target, agent_spinner), daemon=True).start()
    
            user_input.disabled = False
            send_btn.disabled = False
            page.update()
            
        import threading
        threading.Thread(target=run_ai, daemon=True).start()

    send_btn = premium_button("Enviar", "#1976D2", "#2196F3", process_input, icon="send")
    chat_view = ft.Column([chat_list, ft.Container(content=ft.Row([user_input, send_btn]), padding=20)], expand=True)

    # ==========================================
    # 2. CHAT DE EVOLUCION (Meta-Agente Evo)
    # ==========================================
    evo_list = ft.ListView(expand=True, spacing=15, auto_scroll=True, padding=20)
    evo_input = ft.TextField(
        hint_text="Ej: Crea a Max experto en C++... Prueba a Fani... Elimina a Tobi...", 
        expand=True, border_color=COLORS["evo"], multiline=True, min_lines=1, max_lines=5, border_radius=10
    )
    
    def process_evo_input(e):
        text = evo_input.value
        if not text: return
        
        evo_input.value = ""
        evo_input.disabled = True
        evo_send_btn.disabled = True
        add_message(evo_list, "Usuario", text, COLORS["user"])
        
        spinner = ft.Row([ft.ProgressRing(width=20, height=20, color=COLORS["evo"]), ft.Text("Evo procesando arquitectura...", color=COLORS["evo"], italic=True)])
        evo_list.controls.append(spinner)
        page.update()
        
        decision = evo.analyze_request(text)
        evo_list.controls.remove(spinner)
        
        if decision.get("action") == "respond":
            add_message(evo_list, "Evo", decision.get("message", ""), COLORS["evo"])
        elif decision.get("action") == "update_agent":
            a_name = decision.get("agent_name")
            p_content = decision.get("prompt_content")
            add_message(evo_list, "Evo", f"He preparado la matriz para {a_name}. ¿Deseas inyectarla?", COLORS["evo"])
            
            md_text = f"**Nueva Matriz para `{a_name.upper()}`:**\n```markdown\n{p_content}\n```"
            card_content = ft.Column([ft.Markdown(md_text, selectable=True, extension_set="gitHubWeb")])
            
            def on_inject(e):
                btn_inject.disabled = True
                btn_cancel.disabled = True
                btn_row.controls.append(ft.ProgressRing(width=20, height=20, color=COLORS["evo"]))
                page.update()
                try:
                    res = evo.execute_update(a_name, p_content)
                    card_content.controls.append(ft.Text(f"🧬 Éxito: {res}", color="#AB47BC"))
                except Exception as ex:
                    card_content.controls.append(ft.Text(f"❌ Error: {str(ex)}", color="#EF5350"))
                btn_row.controls.pop()
                page.update()

            def on_cancel(e):
                btn_inject.disabled = True
                btn_cancel.disabled = True
                card_content.controls.append(ft.Text("🛑 Inyección Cancelada", color="#EF5350"))
                page.update()

            btn_inject = premium_button("Inyectar Conocimiento", "#8E24AA", "#AB47BC", on_inject, icon="science")
            btn_cancel = premium_button("Cancelar", "#424242", "#616161", on_cancel)
            btn_row = ft.Row([btn_inject, btn_cancel])
            card_content.controls.append(btn_row)
            
            evo_list.controls.append(create_glass_container(card_content, border_color=COLORS["evo"]))
            
        elif decision.get("action") == "delete_agent":
            a_name = decision.get("agent_name")
            add_message(evo_list, "Evo", f"¿Estás seguro de que deseas ELIMINAR permanentemente a {a_name}?", COLORS["evo"])
            
            card_content = ft.Column([])
            def on_delete(e):
                btn_del.disabled = True
                btn_cancel_del.disabled = True
                try:
                    res = evo.execute_delete(a_name)
                    card_content.controls.append(ft.Text(f"🗑️ {res}", color="#EF5350"))
                except Exception as ex:
                    card_content.controls.append(ft.Text(f"❌ Error: {str(ex)}", color="#EF5350"))
                page.update()

            def on_cancel_del(e):
                btn_del.disabled = True
                btn_cancel_del.disabled = True
                card_content.controls.append(ft.Text("🛑 Purga Cancelada", color="grey"))
                page.update()

            btn_del = premium_button("Purgar Agente", "#C62828", "#D32F2F", on_delete, icon="delete_forever")
            btn_cancel_del = premium_button("Cancelar", "#424242", "#616161", on_cancel_del)
            card_content.controls.append(ft.Row([btn_del, btn_cancel_del]))
            evo_list.controls.append(create_glass_container(card_content, border_color="red"))
            
        elif decision.get("action") == "test_agent":
            a_name = decision.get("agent_name")
            p_test = decision.get("prompt_test")
            add_message(evo_list, "Evo", f"Probando a {a_name.upper()} con: '{p_test}'", COLORS["evo"])
            
            test_spinner = ft.Row([ft.ProgressRing(width=20, height=20, color="green"), ft.Text(f"Simulando a {a_name}...", color="green", italic=True)])
            evo_list.controls.append(test_spinner)
            page.update()
            try:
                tester_agent = UniversalAgent(a_name)
                plan = tester_agent.generate_plan(p_test)
                evo_list.controls.remove(test_spinner)
                if "error" in plan:
                    add_message(evo_list, "Evo", f"Error en simulación: {plan['error']}", "red")
                else:
                    md_text = f"**Resultado Simulado `{a_name.upper()}`:**\n```json\n{json.dumps(plan, indent=2)}\n```"
                    evo_list.controls.append(create_glass_container(ft.Markdown(md_text, selectable=True, extension_set="gitHubWeb"), border_color="green"))
            except Exception as ex:
                if test_spinner in evo_list.controls: evo_list.controls.remove(test_spinner)
                add_message(evo_list, "Evo", f"Fallo al invocar agente de prueba: {str(ex)}", "red")
        else:
            add_message(evo_list, "Evo", f"Respuesta no reconocida: {decision}", COLORS["evo"])
            
        evo_input.disabled = False
        evo_send_btn.disabled = False
        evo_input.focus()
        page.update()

    evo_send_btn = premium_button("Enviar a Evo", "#8E24AA", "#AB47BC", process_evo_input, icon="send")
    evolution_view = ft.Column([
        ft.Container(ft.Text("Laboratorio de Evolución (Meta-Agente EVO)", size=20, weight=ft.FontWeight.BOLD, color=COLORS["evo"]), padding=20),
        evo_list, 
        ft.Container(ft.Row([evo_input, evo_send_btn]), padding=20)
    ], expand=True)

    # ==========================================
    # 3. PESTAÑA DE CONFIGURACIÓN
    # ==========================================
    gemini_key_input = ft.TextField(label="GEMINI_API_KEY", value=config.get("GEMINI_API_KEY"), password=True, can_reveal_password=True, border_radius=10)
    azure_org_input = ft.TextField(label="AZURE_DEVOPS_ORG", value=config.get("AZURE_DEVOPS_ORG"), hint_text="Ej: https://dev.azure.com/mi_org", border_radius=10)
    azure_pat_input = ft.TextField(label="AZURE_DEVOPS_PAT", value=config.get("AZURE_DEVOPS_PAT"), password=True, can_reveal_password=True, border_radius=10)
    
    def save_settings(e):
        config.set("GEMINI_API_KEY", gemini_key_input.value)
        config.set("AZURE_DEVOPS_ORG", azure_org_input.value)
        config.set("AZURE_DEVOPS_PAT", azure_pat_input.value)
        page.overlay.append(ft.SnackBar(ft.Text("✅ Configuración cifrada guardada exitosamente."), bgcolor="#388E3C", open=True))
        page.update()

    settings_save_btn = premium_button("Guardar Configuración Cifrada", "#0277BD", "#039BE5", save_settings, icon="security")
    
    config_content = ft.Column([
        ft.Text("Bóveda de Credenciales (Local)", size=24, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text("Tus tokens son encriptados con Fernet (Criptografía Simétrica) y guardados offline.", color="grey"),
        ft.Divider(color="grey"),
        gemini_key_input,
        azure_org_input,
        azure_pat_input,
        ft.Container(height=10),
        settings_save_btn
    ], spacing=15)
    
    config_view = ft.Container(content=create_glass_container(config_content), padding=40, expand=True)

    # ==========================================
    # CONTENEDOR PRINCIPAL Y GRADIENTE
    # ==========================================
    main_content = ft.Container(content=chat_view, expand=True)
    
    # Efecto Background Gradient
    bg_gradient = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[COLORS["bg_start"], COLORS["bg_end"]]
        ),
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text("Gini V5.1 | Hub de Inteligencia Artificial", size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Row([
                        premium_button("Chat Central", "#1E88E5", "#2196F3", lambda e: switch_view(chat_view), icon="chat"),
                        premium_button("Laboratorio (Evo)", "#8E24AA", "#AB47BC", lambda e: switch_view(evolution_view), icon="science"),
                        premium_button("Seguridad", "#424242", "#616161", lambda e: switch_view(config_view), icon="security"),
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=20,
                bgcolor="#40000000" # Header semitransparente
            ),
            main_content
        ], expand=True, spacing=0)
    )

    def switch_view(view):
        main_content.content = view
        page.update()

    page.add(bg_gradient)
    add_message(chat_list, "Gini", "¡Hola! Sistema V5.1 en línea. El entorno ha sido modernizado y los controles de interacción ahora son asincrónicos.", COLORS["gini"])
    add_message(evo_list, "Evo", "Laboratorio activado. Puedes probar o mutar agentes desde aquí.", COLORS["evo"])

if __name__ == "__main__":
    ft.app(target=main)
