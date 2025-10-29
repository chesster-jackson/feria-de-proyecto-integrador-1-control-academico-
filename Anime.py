from colorama import Fore, Style, init
import sys
import time

init(autoreset=True)

def animacion(mensaje="Inicializando el sistema"):
    try:
        print(Fore.GREEN + "\n" + "="*60)
        print(Fore.GREEN + f"🔧 {mensaje}...".center(60))
        print(Fore.GREEN + "="*60)

        anim = ["|", "/", "-", "\\"]
        for i in range(12):
            sys.stdout.write("\r" + Fore.GREEN + "⏳ Procesando, por favor espere... " + anim[i % len(anim)])
            sys.stdout.flush()
            time.sleep(0.12)

        print("\r" + Fore.GREEN + "✅ El sistema se ha iniciado correctamente. Espere un momento...         ")
        time.sleep(0.6)
    except Exception:
        pass
