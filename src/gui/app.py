import uvicorn
import webbrowser
import time
import threading

def open_browser():
    # Pequeño delay para asegurar que el servidor levantó
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")

def main():
    print("Iniciando Gini V8.0 (Zero-Node WebUI)...")
    
    # Inicia el thread para abrir el navegador
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Ejecuta la API de FastAPI
    uvicorn.run("src.gui.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
