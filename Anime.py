import re
import time
import sys
from colorama import Fore, Style, init

def animacion(mensaje="Inicializando el sistema"):
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.YELLOW + f"🔧 {mensaje}...".center(60))
    print(Fore.CYAN + "="*60)

    animacion = ["|", "/", "-", "\\"]
    for i in range(20):
        sys.stdout.write("\r" + Fore.GREEN + "⏳ Procesando, por favor espere... " + animacion[i % len(animacion)])
        sys.stdout.flush()
        time.sleep(0.15)

    print("\r✅ El sistema se ha iniciado correctamente. Espere un momento...         ")
    time.sleep(0.8)
