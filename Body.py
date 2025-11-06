#Cuerpo del programa
import re
import json
import os
from datetime import datetime
from Anime import animacion, Fore, Style, init
from Generador import generar_PDF
from collections import deque

#Esto sirve para que cunad alguien escriba salir salga y lo nombramos asi salirOperacion
class SalirOperacion(Exception):
    pass

cola_pendientes = deque()
pila_acciones = []
estudiantes = []

#Aqui guardamos datos de todo lo que agreguemos  y aqui tambine creamos los j.son
def guardar_datos():
    with open("estudiantes.json", "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, indent=4, ensure_ascii=False)
    with open("pendientes.json", "w", encoding="utf-8") as f:
        json.dump(list(cola_pendientes), f, indent=4, ensure_ascii=False)
    with open("historial.json", "w", encoding="utf-8") as f:
        json.dump(pila_acciones, f, indent=4, ensure_ascii=False)

#aqui cargamos los datos antes de iniciar el programa
def cargar_datos():
    global estudiantes, cola_pendientes, pila_acciones
    if os.path.exists("estudiantes.json"):
        try:
            with open("estudiantes.json", "r", encoding="utf-8") as f:
                estudiantes = json.load(f)
        except Exception:
            estudiantes = []
    if os.path.exists("pendientes.json"):
        try:
            with open("pendientes.json", "r", encoding="utf-8") as f:
                cola_pendientes = deque(json.load(f))
        except Exception:
            cola_pendientes = deque()
    if os.path.exists("historial.json"):
        try:
            with open("historial.json", "r", encoding="utf-8") as f:
                pila_acciones = json.load(f)
        except Exception:
            pila_acciones = []

#Esto sirve para que veamos alos estudiantes que no han echo sus PDF
def encolar_estudiante(est):
    cola_pendientes.append(est)
    print(f" {est['nombre']} {est['apellido']} agregado a la cola de los estudiantes que aun no han echo un documento pdf de sus notas.")
    guardar_datos()

#Esto es lo mismo de que los PDF de tal persona no hemos echo 
def mostrar_pendientes():
    if not cola_pendientes:
        print(" No hay estudiantes pendientes.")
        return
    print("\n COLA DE ESTUDIANTES PENDIENTES:")
    for i, est in enumerate(cola_pendientes, start=1):
        print(f"{i}. {est['nombre']} {est['apellido']} - {est['carnet']}")

#Aqui lo que hacemos es simple si escribe salir sale y si escrbe atras va asia atras
def pedir_dato_confirmar(prompt, tipo=str, validar=None, ejemplo=None, mayus=False, obligatorio=True):
    while True:
        raw = input(f"   {prompt}: ").strip()
        if raw.lower() == "salir":
            raise KeyboardInterrupt
        if raw.lower() == "atras":
            return "ATRAS"
        if obligatorio and raw == "":
            print("    Este campo no puede quedar vacío.")
            continue
        try:
            if tipo == int:
                valor = int(raw)
            elif tipo == float:
                valor = float(raw)
            else:
                valor = raw.upper() if mayus else raw
        except ValueError:
            print("    Tipo de dato incorrecto. Intenta de nuevo.")
            continue
        if validar and not validar(valor):
            msg = "      Formato inválido."
            if ejemplo:
                msg += f" Ejemplo: {ejemplo}"
            print(msg)
            continue
        return valor


#A  qui al finalizar lo de agregar estudinates confirmamos si lo queremos guardar 
def confirmar_si_no(prompt):
    r = input(f"{prompt} (S = sí / cualquier otra tecla = no): ").strip().upper()
    return r == "S"

#Calcular el promedio
def calcular_promedio(lista_notas):
    if not lista_notas:
        return 0.0
    return round(sum(lista_notas) / len(lista_notas), 2)

#Registro de acciones
def registrar_accion(accion):
    tiempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pila_acciones.append(f"{tiempo} - {accion}")
    guardar_datos()

#Muestra el historial
def mostrar_historial():
    if not pila_acciones:
        print(" No hay acciones registradas aún.")
        return
    print("\n HISTORIAL DE ACCIONES (últimas 10):")
    for i, acc in enumerate(reversed(pila_acciones[-10:]), start=1):
        print(f"{i}. {acc}")

#Aqui agregamos alos estudiantes
def agregar_estudiante():
    try:
        print("\n" + "="*70)
        print(" REGISTRO DE NUEVOS ESTUDIANTES")
        print("="*70)
        cantidad_estudiantes = pedir_dato_confirmar("¿Cuántos estudiantes deseas agregar?", int, validar=lambda x: x > 0, ejemplo="1")
        for i in range(1, cantidad_estudiantes + 1):
            print("\n" + "-"*60)
            print(f" Estudiante {i}")
            print("-"*60)

            datos = {
                "nombre": None, "apellido": None, "cedula": None, "carnet": None,
                "municipio": None, "departamento": None, "edad": None, "genero": None,
                "sangre": None, "modalidad": None, "situacion": None, "carrera": None,
                "anio": None, "ciclo": None, "parcial": None, "area": None,
                "idiomas": [], "materias": []
            }

            pasos = [
                ("nombre", lambda: pedir_dato_confirmar("Nombre", str, mayus=True)),
                ("apellido", lambda: pedir_dato_confirmar("Apellido", str, mayus=True)),
                ("cedula", lambda: pedir_dato_confirmar("Cédula (000-000000-0000A)", str,
                    validar=lambda v: bool(re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", v)), ejemplo="001-123456-0000A", mayus=True)),
                ("carnet", lambda: pedir_dato_confirmar("Carnet (25-00000-0)", str,
                    validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-0", v)), ejemplo="25-02365-0")),
                ("municipio", lambda: pedir_dato_confirmar("Municipio", str, mayus=True)),
                ("departamento", lambda: pedir_dato_confirmar("Departamento", str, mayus=True)),
                ("edad", lambda: pedir_dato_confirmar("Edad", int, validar=lambda x: 12 <= x <= 80, ejemplo="12 hasta 80")),
                ("genero", lambda: ("Masculino" if pedir_dato_confirmar("Género (1. Masculino / 2. Femenino)",
                    str, validar=lambda s: s in ["1", "2"]) == "1" else "Femenino")),
                ("sangre", lambda: pedir_dato_confirmar("Tipo de sangre (A+, A-, B+, B-, AB+, AB-, O+, O-)", str, mayus=True,
                    validar=lambda v: bool(re.fullmatch(r"^(A|B|AB|O)[+-]$", v.upper())), ejemplo="O+")),
                ("modalidad", lambda: {"1": "Presencial", "2": "Virtual", "3": "Mixta"}[
                    pedir_dato_confirmar("Modalidad (1. Presencial / 2. Virtual / 3. Mixta)", str, validar=lambda s: s in ["1", "2", "3"])]),
                ("situacion", lambda: {"1": "Regular", "2": "Sabatino", "3": "Dominical"}[
                    pedir_dato_confirmar("Situación académica (1. Regular / 2. Sabatino / 3. Dominical)", str, validar=lambda s: s in ["1", "2", "3"])]),
                ("carrera", lambda: pedir_dato_confirmar("Carrera", str, mayus=True)),
                ("anio", lambda: pedir_dato_confirmar(
                    "¿En qué año de tu carrera estás? (1-5)", 
                                                    int, 
                                                    validar=lambda x: 1 <= x <= 5, 
                                                    ejemplo="1"
                )),

                ("ciclo", lambda: pedir_dato_confirmar(
                    f"Actualmente estás en el ciclo {(datos['anio']-1)*2+1} o {(datos['anio']-1)*2+2}", 
                                                    int, 
                                                    validar=lambda x: x in [(datos['anio']-1)*2+1, (datos['anio']-1)*2+2], 
                                                    ejemplo=f"{(datos['anio']-1)*2+1} o {(datos['anio']-1)*2+2}"
                )),

                ("parcial", lambda: pedir_dato_confirmar(
                    "¿En qué parcial estás actualmente? (1 o 2)", 
                    int, 
                    validar=lambda x: x in [1, 2], 
                    ejemplo="1"
                )),
                ("area", lambda: pedir_dato_confirmar("Área de conocimiento", str, mayus=True)),
            ]

            idx = 0
            while idx < len(pasos):
                campo, funcion = pasos[idx]
                valor = funcion()
                if valor == "ATRAS":
                    if idx > 0:
                        idx -= 1
                        continue
                    else:
                        print("   Ya estás en el primer dato.")
                        continue
                datos[campo] = valor
                idx += 1

            idiomas_cant = pedir_dato_confirmar("¿Cuántos idiomas domina? (mínimo 1)", int, validar=lambda x: x >= 1, ejemplo="1")
            for j in range(1, idiomas_cant + 1):
                idioma = pedir_dato_confirmar(f"Idioma {j}", str, mayus=True)
                if idioma == "ATRAS":
                    if j > 1:
                        j -= 1
                        continue
                    else:
                        print("    No se puede retroceder más en idiomas.")
                        continue
                datos["idiomas"].append(idioma)

            materias_cant = pedir_dato_confirmar("¿Cuántas materias cursa este estudiante?", int, validar=lambda x: x > 0, ejemplo="2")
            mostrar_c2 = True if datos["ciclo"] % 2 == 0 else False

            for m in range(1, materias_cant + 1):
                print("\n" + "-"*40)
                print(f" Materia {m}")
                nombre_mat = pedir_dato_confirmar(f"Nombre de la materia {m}", str, mayus=True)
                notas = {}
                print(f" Ingresando notas para {nombre_mat}:")
                notas["C1P1"] = pedir_dato_confirmar("Ciclo 1 - Parcial 1 (0-100)", float, validar=lambda x: 0 <= x <= 100)
                notas["C1P2"] = pedir_dato_confirmar("Ciclo 1 - Parcial 2 (0-100)", float, validar=lambda x: 0 <= x <= 100)
                if mostrar_c2:
                    notas["C2P1"] = pedir_dato_confirmar("Ciclo 2 - Parcial 1 (0-100)", float, validar=lambda x: 0 <= x <= 100)
                    notas["C2P2"] = pedir_dato_confirmar("Ciclo 2 - Parcial 2 (0-100)", float, validar=lambda x: 0 <= x <= 100)
                promedio_mat = calcular_promedio([v for v in notas.values()])
                estado_mat = "Aprobado" if promedio_mat >= 60 else "Reprobado"
                datos["materias"].append({"materia": nombre_mat, "notas": notas, "promedio": promedio_mat, "estado": estado_mat})

            promedio_general = calcular_promedio([m["promedio"] for m in datos["materias"]])
            estado_final = "Aprobado" if promedio_general >= 60 else "Reprobado"

            print("\n" + "="*60)
            print("RESUMEN DEL ESTUDIANTE")
            print("="*60)
            print(f"Nombre:             {datos['nombre']}")
            print(f"Apellido:           {datos['apellido']}")
            print(f"Cédula:             {datos['cedula']}")
            print(f"Carnet:             {datos['carnet']}")
            print(f"Carrera:            {datos['carrera']}")
            print(f"Año:                {datos['anio']}")
            print(f"Ciclo:              {datos['ciclo']}")
            print(f"Parcial:            {datos['parcial']}")
            print(f"Idiomas:            {', '.join(datos['idiomas'])}")
            print("Materias:")
            for mat in datos["materias"]:
                print(f"    • {mat['materia']}")
                notas = mat["notas"]
                print(f"        C1P1 = {notas.get('C1P1','')}   C1P2 = {notas.get('C1P2','')}")
                if 'C2P1' in notas or 'C2P2' in notas:
                    print(f"        C2P1 = {notas.get('C2P1','')}   C2P2 = {notas.get('C2P2','')}")
                print(f"        Promedio: {mat['promedio']:.2f}   Estado: {mat['estado']}")
            print(f"Índice general:     {promedio_general:.2f}")
            print(f"Estado final:       {estado_final}")

            if not confirmar_si_no("¿Deseas confirmar y guardar este estudiante?"):
                continue

            fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            estudiante = {**datos, "promedio": promedio_general, "fecha_registro": fecha_registro, "ultima_modificacion": None}
            estudiantes.append(estudiante)
            encolar_estudiante(estudiante)
            registrar_accion(f"Se agregó a {datos['nombre']} {datos['apellido']} con carnet {datos['carnet']}")
            registrar_accion(f"{datos['nombre']} {datos['apellido']} agregado a la cola de pendientes")
            guardar_datos()

    except KeyboardInterrupt:
        print("\n Operación cancelada. Regresando al menú principal...")
        return



#Aqui mostramos todos los estudiantes agregados
def mostrar_lista():
    if not estudiantes:
        print(" No hay estudiantes registrados.")
        return
    print("\n" + "="*60)
    print(" LISTA COMPLETA DE ESTUDIANTES")
    print("="*60)
    for idx, est in enumerate(estudiantes, start=1):
        print("\n" + "-"*60)
        print(f"#{idx}")
        print(f"{'Nombre:':<20}{est['nombre']}")
        print(f"{'Apellido:':<20}{est['apellido']}")
        print(f"{'Carnet:':<20}{est['carnet']}")
        print(f"{'Carrera:':<20}{est['carrera']}")
        print(f"{'Municipio:':<20}{est['municipio']}")
        print(f"{'Departamento:':<20}{est['departamento']}")
        print(f"{'Año:':<20}{est['anio']}")
        print(f"{'Ciclo:':<20}{est['ciclo']}")
        print(f"{'ciclo actual:':<20}{est['parcial']}")
        print(f"{'Idiomas:':<20}{', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
        print(" MATERIAS Y NOTAS:")
        for m in est['materias']:
            notas = m['notas']
            print(f"   • {m['materia']}")
            if notas.get('C2P1') is not None or notas.get('C2P2') is not None:
                print(f"{'':8}C1P1 = {notas.get('C1P1','')}   C1P2 = {notas.get('C1P2','')}   C2P1 = {notas.get('C2P1','')}   C2P2 = {notas.get('C2P2','')}")
            else:
                print(f"{'':8}C1P1 = {notas.get('C1P1','')}   C1P2 = {notas.get('C1P2','')}")
            print(f"{'':8}Promedio: {m['promedio']:.2f}   Estado: {m['estado']}")
        print(f"{'Índice Académico:':<20}{est.get('promedio',0):.2f}")
        print(f"{'Estado final:':<20}{'Aprobado ' if est.get('promedio',0)>=60 else 'Reprobado '}")
        print(f"{'Registrado el:':<20}{est.get('fecha_registro')}")
        print(f"{'Última modif.:':<20}{est.get('ultima_modificacion')}")
        print("-"*60)



#Aqui buscamos alos estudiantes
def buscar_estudiante():
    try:
        carnet = pedir_dato_confirmar(
            "Ingrese el carnet a buscar (25-00000-0)", 
            str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-0", v)),
            ejemplo="25-00001-0"
        )
        encontrado = next((e for e in estudiantes if e["carnet"] == carnet), None)
        if not encontrado:
            print(" Estudiante no encontrado.")
            return
        print("\n" + "="*50)
        print(f"{'Nombre:':<20}{encontrado['nombre']}")
        print(f"{'Apellido:':<20}{encontrado['apellido']}")
        print(f"{'Carnet:':<20}{encontrado['carnet']}")
        print(f"{'Cédula:':<20}{encontrado['cedula']}")
        print(f"{'Carrera:':<20}{encontrado['carrera']}")
        print(f"{'Año:':<20}{encontrado['anio']}")
        print(f"{'Ciclo:':<20}{encontrado['ciclo']}")
        print(f"{'Parcial:':<20}{encontrado['parcial']}")
        print(f"{'Municipio:':<20}{encontrado['municipio']}")
        print(f"{'Departamento:':<20}{encontrado['departamento']}")
        print(f"{'Género:':<20}{encontrado['genero']}")
        print(f"{'Sangre:':<20}{encontrado['sangre']}")
        print(f"{'Área:':<20}{encontrado['area']}")
        print(f"{'Idiomas:':<20}{', '.join(encontrado['idiomas']) if encontrado['idiomas'] else 'Ninguno'}")
        print("\n MATERIAS:")
        for m in encontrado['materias']:
            notas = m['notas']
            print(f"   • {m['materia']}")
            if notas.get('C2P1') is not None or notas.get('C2P2') is not None:
                print(f"{'':8}C1P1 = {notas.get('C1P1','')}   C1P2 = {notas.get('C1P2','')}   C2P1 = {notas.get('C2P1','')}   C2P2 = {notas.get('C2P2','')}")
            else:
                print(f"{'':8}C1P1 = {notas.get('C1P1','')}   C1P2 = {notas.get('C1P2','')}")
            print(f"{'':8}Promedio: {m['promedio']:.2f}   Estado: {m['estado']}")
        print(f"\n{'Índice Académico:':<20}{encontrado.get('promedio',0):.2f}")
        print(f"{'Estado final:':<20}{'Aprobado ' if encontrado.get('promedio',0)>=60 else 'Reprobado '}")
        print(f"{'Registrado:':<20}{encontrado.get('fecha_registro')}")
        print(f"{'Última modif.:':<20}{encontrado.get('ultima_modificacion')}")
        print("="*50)
        while True:
            print("\n¿Qué deseas hacer con este registro?")
            print("1. Editar datos")
            print("2. Eliminar estudiante")
            print("3. Volver al menú")
            op = input("Elige (1-3): ").strip()
            if op == "1":
                editar_estudiante(encontrado)
                break
            elif op == "2":
                eliminar_estudiante(encontrado['carnet'])
                break
            elif op == "3":
                return
            else:
                print(" Opción inválida. Usa 1, 2 o 3.")
    except SalirOperacion:
        print("\n Búsqueda cancelada. Regresando al menú principal...")


#Aqui los eliminamos por numero de carnet
def eliminar_estudiante(carnet=None):
    try:
        if not carnet:
            carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante a eliminar (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-0", v)), ejemplo="25-02365-0")
        for i, est in enumerate(estudiantes):
            if est["carnet"] == carnet:
                confirmar = confirmar_si_no(f"¿Seguro que deseas eliminar a {est['nombre']} {est['apellido']}?")
                if confirmar:
                    del estudiantes[i]
                    for p in list(cola_pendientes):
                        if p.get("carnet") == carnet:
                            cola_pendientes.remove(p)
                    registrar_accion(f"Se eliminó a {est['nombre']} {est['apellido']} ({carnet})")
                    guardar_datos()
                    print(" Estudiante eliminado correctamente.")
                else:
                    print(" Operación cancelada. No se eliminó.")
                return
        print(" Estudiante no encontrado.")
    except SalirOperacion:
        print("\n Eliminación cancelada. Regresando al menú...")

#Aqui editamos el campo que queramos del estudinate
def editar_estudiante(est):
    try:
        while True:
            print("\n" + "-"*50)
            print(f" Editando: Nombre {est['nombre']} | apellido {est['apellido']}  |  Carnet: {est['carnet']}")
            print("1. Nombre")
            print("2. Apellido")
            print("3. Cédula")
            print("4. Carnet")
            print("5. Municipio")
            print("6. Departamento")
            print("7. Edad")
            print("8. Género")
            print("9. Tipo de sangre")
            print("10. Modalidad")
            print("11. Situación académica")
            print("12. Carrera")
            print("13. Año")
            print("14. Ciclo")
            print("15. Parcial")
            print("16. Área de conocimiento")
            print("17. Idiomas")
            print("18. Materias (agregar/quitar)")
            print("19. Editar notas de una materia")
            print("20. Volver")
            opc = input("Elige (1-20): ").strip()
            if opc == "1":
                nuevo = pedir_dato_confirmar("Nuevo nombre", str, mayus=True)
                est["nombre"] = nuevo
                registrar_accion(f"Se editó el nombre de {est['carnet']}")
                print(" Nombre actualizado.")
            elif opc == "2":
                nuevo = pedir_dato_confirmar("Nuevo apellido", str, mayus=True)
                est["apellido"] = nuevo
                registrar_accion(f"Se editó el apellido de {est['carnet']}")
                print(" Apellido actualizado.")
            elif opc == "3":
                nuevo = pedir_dato_confirmar("Nueva cédula (000-000000-0000A)", str, validar=lambda v: bool(re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", v)), ejemplo="001-123456-0000A", mayus=True)
                est["cedula"] = nuevo
                registrar_accion(f"Se editó la cédula de {est['carnet']}")
                print(" Cédula actualizada.")
            elif opc == "4":
                while True:
                    nuevo = pedir_dato_confirmar("Nuevo carnet (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-00000-0")
                    if any(e["carnet"] == nuevo and e is not est for e in estudiantes):
                        print(" Ya existe otro estudiante con ese carnet. Intenta otro.")
                    else:
                        est["carnet"] = nuevo
                        registrar_accion(f"Se cambió carnet a {nuevo}")
                        print(" Carnet actualizado.")
                        break
            elif opc == "5":
                nuevo = pedir_dato_confirmar("Nuevo municipio", str, mayus=True)
                est["municipio"] = nuevo
                registrar_accion(f"Se editó municipio de {est['carnet']}")
                print(" Municipio actualizado.")
            elif opc == "6":
                nuevo = pedir_dato_confirmar("Nuevo departamento", str, mayus=True)
                est["departamento"] = nuevo
                registrar_accion(f"Se editó departamento de {est['carnet']}")
                print(" Departamento actualizado.")
            elif opc == "7":
                nuevo = pedir_dato_confirmar("Nueva edad", int, validar=lambda x: 12 <= x <= 80, ejemplo="20")
                est["edad"] = nuevo
                registrar_accion(f"Se editó edad de {est['carnet']}")
                print(" Edad actualizada.")
            elif opc == "8":
                nuevo = pedir_dato_confirmar("Género (1. Masculino / 2. Femenino)", str, validar=lambda s: s in ["1","2"])
                est["genero"] = "Masculino" if nuevo == "1" else "Femenino"
                registrar_accion(f"Se editó género de {est['carnet']}")
                print(" Género actualizado.")
            elif opc == "9":
                nuevo = pedir_dato_confirmar("Nuevo tipo de sangre (A+, O-, AB-, ...)", str, validar=lambda v: bool(re.fullmatch(r"(A|B|AB|O)[+-]", v)), mayus=True)
                est["sangre"] = nuevo
                registrar_accion(f"Se editó sangre de {est['carnet']}")
                print(" Tipo de sangre actualizado.")
            elif opc == "10":
                op = pedir_dato_confirmar("Modalidad (1. Presencial / 2. Virtual / 3. Mixta)", str, validar=lambda s: s in ["1","2","3"])
                est["modalidad"] = {"1": "Presencial", "2": "Virtual", "3": "Mixta"}[op]
                registrar_accion(f"Se editó modalidad de {est['carnet']}")
                print(" Modalidad actualizada.")
            elif opc == "11":
                op = pedir_dato_confirmar("Situación académica (1. Regular / 2. Sabatino / 3. Dominical)", str, validar=lambda s: s in ["1","2","3"])
                est["situacion"] = {"1": "Regular", "2": "Sabatino", "3": "Dominical"}[op]
                registrar_accion(f"Se editó situación de {est['carnet']}")
                print(" Situación actualizada.")
            elif opc == "12":
                nuevo = pedir_dato_confirmar("Nueva carrera", str, mayus=True)
                est["carrera"] = nuevo
                registrar_accion(f"Se editó carrera de {est['carnet']}")
                print(" Carrera actualizada.")
            elif opc == "13":
                nuevo = pedir_dato_confirmar("Nuevo año (1-6)", int, validar=lambda x: 1 <= x <= 6)
                est["anio"] = nuevo
                registrar_accion(f"Se editó año de {est['carnet']}")
                print(" Año actualizado.")
            elif opc == "14":
                nuevo = pedir_dato_confirmar("Nuevo ciclo (1–11)", int, validar=lambda x: 1 <= x <= 11)
                est["ciclo"] = nuevo
                registrar_accion(f"Se editó ciclo de {est['carnet']}")
                print(" Ciclo actualizado.")
            elif opc == "15":
                nuevo = pedir_dato_confirmar("Nuevo parcial (1 o 2)", int, validar=lambda x: x in [1,2])
                est["parcial"] = nuevo
                registrar_accion(f"Se editó parcial de {est['carnet']}")
                print(" Parcial actualizado.")
            elif opc == "16":
                nuevo = pedir_dato_confirmar("Nueva área de conocimiento", str, mayus=True)
                est["area"] = nuevo
                registrar_accion(f"Se editó área de {est['carnet']}")
                print(" Área actualizada.")
            elif opc == "17":
                cant = pedir_dato_confirmar("¿Cuántos idiomas ahora?", int, validar=lambda x: x>=0)
                idiomas = []
                for j in range(1, cant+1):
                    idi = pedir_dato_confirmar(f"Idioma {j}", str, mayus=True)
                    idiomas.append(idi)
                est["idiomas"] = idiomas
                registrar_accion(f"Se editaron idiomas de {est['carnet']}")
                print(" Idiomas actualizados.")
            elif opc == "18":
                print("1. Agregar materia")
                print("2. Quitar materia")
                opm = input("Elige (1-2): ").strip()
                if opm == "1":
                    nombre_n = pedir_dato_confirmar("Nombre de la nueva materia", str, mayus=True)
                    notas = {}
                    notas["C1P1"] = pedir_dato_confirmar(f"C1P1 (0-100)", float, validar=lambda x: 0<=x<=100)
                    notas["C1P2"] = pedir_dato_confirmar(f"C1P2 (0-100)", float, validar=lambda x: 0<=x<=100)
                    if est.get("ciclo",1) % 2 == 0:
                        notas["C2P1"] = pedir_dato_confirmar(f"C2P1 (0-100)", float, validar=lambda x: 0<=x<=100)
                        notas["C2P2"] = pedir_dato_confirmar(f"C2P2 (0-100)", float, validar=lambda x: 0<=x<=100)
                    prom = calcular_promedio(list(notas.values()))
                    estado = "Aprobado" if prom >= 60 else "Reprobado"
                    est['materias'].append({"materia": nombre_n, "notas": notas, "promedio": prom, "estado": estado})
                    registrar_accion(f"Se agregó materia a {est['carnet']}")
                    print(" Materia agregada.")
                elif opm == "2":
                    if not est['materias']:
                        print(" No hay materias para quitar.")
                    else:
                        for idx, m in enumerate(est['materias'], start=1):
                            print(f"{idx}. {m['materia']}")
                        try:
                            sel = int(input("Seleccione el número de la materia a quitar: ").strip())
                            if 1 <= sel <= len(est['materias']):
                                borr = est['materias'].pop(sel-1)
                                registrar_accion(f"Se quitó materia de {est['carnet']}")
                                print(f"🗑 Materia {borr['materia']} eliminada.")
                            else:
                                print(" Selección inválida.")
                        except ValueError:
                            print(" Ingresa un número válido.")
                else:
                    print(" Opción inválida.")
            elif opc == "19":
                if not est['materias']:
                    print(" No hay materias para editar.")
                else:
                    for idx, m in enumerate(est['materias'], start=1):
                        print(f"{idx}. {m['materia']}")
                    try:
                        sel = int(input("Selecciona materia a editar (número): ").strip())
                        if 1 <= sel <= len(est['materias']):
                            mobj = est['materias'][sel-1]
                            notas = mobj['notas']
                            notas["C1P1"] = pedir_dato_confirmar(f"Nueva nota C1P1 (0-100)", float, validar=lambda x: 0<=x<=100)
                            notas["C1P2"] = pedir_dato_confirmar(f"Nueva nota C1P2 (0-100)", float, validar=lambda x: 0<=x<=100)
                            if est.get("ciclo",1) % 2 == 0:
                                notas["C2P1"] = pedir_dato_confirmar(f"Nueva nota C2P1 (0-100)", float, validar=lambda x: 0<=x<=100)
                                notas["C2P2"] = pedir_dato_confirmar(f"Nueva nota C2P2 (0-100)", float, validar=lambda x: 0<=x<=100)
                            mobj['promedio'] = calcular_promedio([v for v in notas.values()])
                            mobj['estado'] = "Aprobado" if mobj['promedio'] >= 60 else "Reprobado"
                            registrar_accion(f"Se editaron notas de {est['carnet']}")
                            print(" Notas actualizadas.")
                        else:
                            print(" Selección inválida.")
                    except ValueError:
                        print(" Ingresa un número válido.")
            elif opc == "20":
                est['ultima_modificacion'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                guardar_datos()
                print(" Volviendo al menú anterior...")
                break
            else:
                print(" Opción inválida. Intente de nuevo.")
            est['ultima_modificacion'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            guardar_datos()
    except SalirOperacion:
        print(" Edición cancelada. Regresando al menú...")

#Desde aqui pasamos la informacion al generador 
def generar_pdf():
    try:
        if not estudiantes:
            print(" No hay estudiantes registrados.")
            return
        carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante para generar su certificado (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-0", v)), ejemplo="25-02365-0")
        encontrado = next((e for e in estudiantes if e['carnet'] == carnet), None)
        if not encontrado:
            print(f" No se encontró al estudiante con carnet {carnet}.")
            return
        nombre_pdf = f"certificado_{encontrado['carnet'].replace('-', '_')}.pdf"
        carnet_generado = generar_PDF(encontrado, nombre_pdf, registrar_accion)
        if carnet_generado:
            for est in list(cola_pendientes):
                if est.get("carnet") == carnet_generado:
                    cola_pendientes.remove(est)
                    print(f" {est['nombre']} {est['apellido']} ({est['carnet']}) eliminado de la cola tras generar PDF.")
                    registrar_accion(f"{est['nombre']} {est['apellido']} ({est['carnet']}) fue removido de la cola tras generar PDF")
                    guardar_datos()
                    break
    except SalirOperacion:
        print("\n Operación cancelada. Regresando al menú...")

    except KeyboardInterrupt:
        print("\n Operación cancelada. Regresando al menú...")