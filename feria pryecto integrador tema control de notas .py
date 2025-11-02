import re
import json
import os
from datetime import datetime
from Anime import animacion, Fore, Style, init
from Generador import generar_PDF
from collections import deque

class SalirOperacion(Exception):
    pass

cola_pendientes = deque()
pila_acciones = []
estudiantes = []

def guardar_datos():
    with open("estudiantes.json", "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, indent=4, ensure_ascii=False)
    with open("pendientes.json", "w", encoding="utf-8") as f:
        json.dump(list(cola_pendientes), f, indent=4, ensure_ascii=False)
    with open("historial.json", "w", encoding="utf-8") as f:
        json.dump(pila_acciones, f, indent=4, ensure_ascii=False)

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

def encolar_estudiante(est):
    cola_pendientes.append(est)
    print(f" {est['nombre']} {est['apellido']} agregado a la cola de los estudiantes que aun no han echo un documento pdf de sus notas.")
    guardar_datos()

def mostrar_pendientes():
    if not cola_pendientes:
        print(" No hay estudiantes pendientes.")
        return
    print("\n COLA DE ESTUDIANTES PENDIENTES:")
    for i, est in enumerate(cola_pendientes, start=1):
        print(f"{i}. {est['nombre']} {est['apellido']} - {est['carnet']}")

def pedir_dato_confirmar(prompt, tipo=str, validar=None, ejemplo=None, mayus=False, obligatorio=True):
    while True:
        raw = input(f"    {prompt}: ").strip()
        if raw.lower() == "salir":
            raise SalirOperacion
        if obligatorio and raw == "":
            print(" Este campo no puede quedar vacío.")
            continue
        try:
            if tipo == int:
                valor = int(raw)
            elif tipo == float:
                valor = float(raw)
            else:
                valor = raw.upper() if mayus else raw
        except ValueError:
            print(" Tipo de dato incorrecto. Intenta de nuevo.")
            continue
        if validar:
            try:
                ok = validar(valor)
            except Exception:
                ok = False
            if not ok:
                msg = "Formato inválido."
                if ejemplo:
                    msg += f" Ejemplo: {ejemplo}"
                print(f" {msg}")
                continue
        while True:
            print(f"  Has ingresado: {valor}")
            print("   ¿Deseas confirmar este dato?")
            print("   1. Confirmar")
            print("   2. Modificar")
            opcion = input("   Elige (1-2): ").strip()
            if opcion == "1":
                return valor
            elif opcion == "2":
                print("    Volvamos a ingresarlo...")
                break
            else:
                print(" Debes ingresar 1 o 2. Intenta de nuevo.")

def confirmar_si_no(prompt):
    r = input(f"{prompt} (S = sí / cualquier otra tecla = no): ").strip().upper()
    return r == "S"

def calcular_promedio(lista_notas):
    if not lista_notas:
        return 0.0
    return round(sum(lista_notas) / len(lista_notas), 2)

def registrar_accion(accion):
    tiempo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pila_acciones.append(f"{tiempo} - {accion}")
    guardar_datos()

def mostrar_historial():
    if not pila_acciones:
        print(" No hay acciones registradas aún.")
        return
    print("\n HISTORIAL DE ACCIONES (últimas 10):")
    for i, acc in enumerate(reversed(pila_acciones[-10:]), start=1):
        print(f"{i}. {acc}")

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
            nombre = pedir_dato_confirmar("Nombre", str, mayus=True)
            apellido = pedir_dato_confirmar("Apellido", str, mayus=True)
            cedula = pedir_dato_confirmar("Cédula (000-000000-0000A)", str, validar=lambda v: bool(re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", v)), ejemplo="001-123456-0000A", mayus=True)
            carnet = pedir_dato_confirmar("Carnet (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-02365-9")
            municipio = pedir_dato_confirmar("Municipio", str, mayus=True)
            departamento = pedir_dato_confirmar("Departamento", str, mayus=True)
            edad = pedir_dato_confirmar("Edad", int, validar=lambda x: 10 <= x <= 100, ejemplo="20")
            op_gen = pedir_dato_confirmar("Género (1. Masculino / 2. Femenino)", str, validar=lambda s: s in ["1","2"])
            genero = "Masculino" if op_gen == "1" else "Femenino"
            tipo_sangre = pedir_dato_confirmar("Tipo de sangre (A+, A-, B+, B-, AB+, AB-, O+, O-)", str, validar=lambda v: bool(re.fullmatch(r"^(A|B|AB|O)[+-]$", v.upper())), ejemplo="O+")
            modalidad = {"1": "Presencial", "2": "Virtual", "3": "Mixta"}[pedir_dato_confirmar("Modalidad (1. Presencial / 2. Virtual / 3. Mixta)", str, validar=lambda s: s in ["1","2","3"])]
            situacion = {"1": "Regular", "2": "Sabatino", "3": "Dominical"}[pedir_dato_confirmar("Situación académica (1. Regular / 2. Sabatino / 3. Dominical)", str, validating:=None) if False else pedir_dato_confirmar("Situación académica (1. Regular / 2. Sabatino / 3. Dominical)", str, validar=lambda s: s in ["1","2","3"])]
            carrera = pedir_dato_confirmar("Carrera", str, mayus=True)
            anio = pedir_dato_confirmar("Año actual (1-6)", int, validar=lambda x: 1 <= x <= 6, ejemplo="1")
            ciclo = pedir_dato_confirmar("Ciclo actual (1–11)", int, validar=lambda x: 1 <= x <= 11, ejemplo="1")
            parcial = pedir_dato_confirmar("Parcial (1 o 2)", int, validar=lambda x: x in [1,2], ejemplo="1")
            area = pedir_dato_confirmar("Área de conocimiento", str, mayus=True)
            idiomas_cant = pedir_dato_confirmar("¿Cuántos idiomas domina? (mínimo 1)", int, validar=lambda x: x >= 1, ejemplo="1")
            idiomas = []
            for idx in range(1, idiomas_cant + 1):
                idi = pedir_dato_confirmar(f"Idioma {idx}", str, mayus=True)
                idiomas.append(idi)
            materias_cant = pedir_dato_confirmar("¿Cuántas materias cursa este estudiante?", int, validar=lambda x: x > 0, ejemplo="2")
            materias = []
            mostrar_c2 = True if ciclo % 2 == 0 else False
            for m in range(1, materias_cant + 1):
                print("\n" + "-"*40)
                print(f" Materia {m}")
                nombre_mat = pedir_dato_confirmar(f"Nombre de la materia {m}", str, mayus=True)
                notas = {}
                print(f" Ingresando notas para {nombre_mat}:")
                valor = pedir_dato_confirmar(f"Ciclo 1 - Parcial 1 (0-100)", float, validar=lambda x: 0 <= x <= 100, ejemplo="88")
                notas["C1P1"] = valor
                valor = pedir_dato_confirmar(f"Ciclo 1 - Parcial 2 (0-100)", float, validar=lambda x: 0 <= x <= 100, ejemplo="88")
                notas["C1P2"] = valor
                if mostrar_c2:
                    valor = pedir_dato_confirmar(f"Ciclo 2 - Parcial 1 (0-100)", float, validar=lambda x: 0 <= x <= 100, ejemplo="88")
                    notas["C2P1"] = valor
                    valor = pedir_dato_confirmar(f"Ciclo 2 - Parcial 2 (0-100)", float, validar=lambda x: 0 <= x <= 100, ejemplo="88")
                    notas["C2P2"] = valor
                promedio_mat = calcular_promedio([v for v in notas.values()])
                estado_mat = "Aprobado" if promedio_mat >= 60 else "Reprobado"
                materias.append({"materia": nombre_mat, "notas": notas, "promedio": promedio_mat, "estado": estado_mat})
                print(f"   Promedio final de {nombre_mat}: {promedio_mat:.2f} | Estado: {estado_mat}")
            promedio_general = calcular_promedio([m["promedio"] for m in materias])
            estado_final = "Aprobado" if promedio_general >= 60 else "Reprobado"
            print("\n" + "="*60)
            print(" RESUMEN DEL ESTUDIANTE")
            print("="*60)
            print(f" Nombre y apellido {nombre} {apellido}")
            print(f" Cedula {cedula} | Carnet {carnet}")
            print(f" Carrera {carrera} | Año: {anio} | Ciclo: {ciclo} | Parcial: {parcial}")
            print(f" Materias: {len(materias)}")
            for mat in materias:
                print(f"   - {mat['materia']}: Promedio {mat['promedio']:.2f} | {mat['estado']}")
            print("-"*60)
            print(f" Índice general: {promedio_general:.2f}")
            print(f" Estado final: {estado_final}")
            if not confirmar_si_no("¿Deseas confirmar y guardar este estudiante?"):
                continue
            fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            estudiante = {"nombre": nombre, "apellido": apellido, "cedula": cedula, "carnet": carnet, "municipio": municipio, "departamento": departamento, "edad": edad, "genero": genero, "sangre": tipo_sangre, "modalidad": modalidad, "situacion": situacion, "carrera": carrera, "anio": anio, "ciclo": ciclo, "parcial": parcial, "area": area, "idiomas": idiomas, "materias": materias, "promedio": promedio_general, "fecha_registro": fecha_registro, "ultima_modificacion": None}
            estudiantes.append(estudiante)
            encolar_estudiante(estudiante)
            registrar_accion(f"Se agregó a {nombre} {apellido} con carnet {carnet}")
            registrar_accion(f"{nombre} {apellido} agregado a la cola de pendientes")
            guardar_datos()
    except SalirOperacion:
        print("\n Operación cancelada. Regresando al menú principal...")
        return

def mostrar_lista():
    if not estudiantes:
        print(" No hay estudiantes registrados.")
        return
    print("\n" + "="*60)
    print(" LISTA COMPLETA DE ESTUDIANTES")
    print("="*60)
    for idx, est in enumerate(estudiantes, start=1):
        print("\n" + "-"*60)
        print(f"#{idx} nombre   {est['nombre']} | apellido {est['apellido']}  |   Carnet: {est['carnet']}")
        print(f" Municipio {est['municipio']} | departamento  {est['departamento']}  |  Carrera: {est['carrera']} (Año {est['anio']}, Ciclo {est['ciclo']})")
        print(f" Idiomas: {', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
        print(" MATERIAS Y NOTAS:")
        for m in est['materias']:
            notas = m['notas']
            line = f"  • {m['materia']}: C1P1={notas.get('C1P1','')} C1P2={notas.get('C1P2','')}"
            if notas.get('C2P1') is not None or notas.get('C2P2') is not None:
                line += f" C2P1={notas.get('C2P1','')} C2P2={notas.get('C2P2','')}"
            line += f" -> Prom: {m['promedio']:.2f} | {m['estado']}"
            print(line)
        print(f" Índice Académico: {est.get('promedio',0):.2f}  |  Estado final: {'Aprobado ' if est.get('promedio',0)>=60 else 'Reprobado '}")
        print(f" Registrado el: {est.get('fecha_registro')}  |  Última modif.: {est.get('ultima_modificacion')}")
        print("-"*60)

def buscar_estudiante():
    try:
        carnet = pedir_dato_confirmar("Ingrese el carnet a buscar (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-02365-9")
        encontrado = next((e for e in estudiantes if e["carnet"] == carnet), None)
        if not encontrado:
            print(" Estudiante no encontrado.")
            return
        print("\n" + "="*50)
        print(f" Nombre y apellido  {encontrado['nombre']}  {encontrado['apellido']}  |  Carnet {encontrado['carnet']}")
        print("="*50)
        print(f" Cédula: {encontrado['cedula']}")
        print(f" Municipio {encontrado['municipio']} | departamento {encontrado['departamento']}")
        print(f" Edad: {encontrado['edad']} | Género: {encontrado['genero']} | Sangre: {encontrado['sangre']}")
        print(f" Carrera: {encontrado['carrera']} | Año: {encontrado['anio']} | Ciclo: {encontrado['ciclo']} | Parcial: {encontrado['parcial']}")
        print(f" Modalidad: {encontrado['modalidad']} | Situación: {encontrado['situacion']}")
        print(f" Área: {encontrado['area']}")
        print(f" Idiomas: {', '.join(encontrado['idiomas']) if encontrado['idiomas'] else 'Ninguno'}")
        print(" MATERIAS:")
        for m in encontrado['materias']:
            notas = m['notas']
            line = f"  • {m['materia']}: C1P1={notas.get('C1P1','')} C1P2={notas.get('C1P2','')}"
            if notas.get('C2P1') is not None or notas.get('C2P2') is not None:
                line += f" C2P1={notas.get('C2P1','')} C2P2={notas.get('C2P2','')}"
            line += f" -> Prom: {m['promedio']:.2f} | {m['estado']}"
            print(line)
        print(f" Índice Académico: {encontrado.get('promedio',0):.2f} | Estado final: {'Aprobado ✅' if encontrado.get('promedio',0)>=60 else 'Reprobado ❌'}")
        print(f" Registrado: {encontrado.get('fecha_registro')}  |  Última modificación: {encontrado.get('ultima_modificacion')}")
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

def eliminar_estudiante(carnet=None):
    try:
        if not carnet:
            carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante a eliminar (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-02365-9")
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
                    nuevo = pedir_dato_confirmar("Nuevo carnet (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-02365-9")
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
                nuevo = pedir_dato_confirmar("Nueva edad", int, validar=lambda x: 10 <= x <= 120, ejemplo="20")
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

def generar_pdf():
    try:
        if not estudiantes:
            print(" No hay estudiantes registrados.")
            return
        carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante para generar su certificado (25-00000-0)", str, validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)), ejemplo="25-02365-9")
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
                    print(Fore.GREEN + f" {est['nombre']} {est['apellido']} ({est['carnet']}) eliminado de la cola tras generar PDF." + Style.RESET_ALL)
                    registrar_accion(f"{est['nombre']} {est['apellido']} ({est['carnet']}) fue removido de la cola tras generar PDF")
                    guardar_datos()
                    break
    except SalirOperacion:
        print("\n Operación cancelada. Regresando al menú...")

def mostrar_menu():
    print("\n" + "="*50)
    print(" MENÚ PRINCIPAL")
    print("="*50)
    print("1. Agregar estudiante")
    print("2. Buscar / Ver / Editar estudiante (por carnet)")
    print("3. Eliminar estudiante (por carnet)")
    print("4. Mostrar lista de estudiantes")
    print("5. Generar certificados PDF")
    print("6. Mostrar historial de acciones")
    print("7. Ver cola de estudiantes pendientes")
    print("8. Salir")



def main():
    cargar_datos()
    print("=" * 60)
    print(" Bienvenido al Sistema de Control de Notas ")
    print("=" * 60)
    try:
        animacion()
    except Exception:
        pass

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-8): ").strip().lower()
        if opcion == "salir" or opcion == "8":
            print(" Gracias por usar el sistema. ¡Hasta pronto!")
            break

        elif opcion == "1":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            try:
                agregar_estudiante()
            except SalirOperacion:
                print(" Regresando al menú principal...")

        elif opcion == "2":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            try:
                buscar_estudiante()
            except SalirOperacion:
                print(" Regresando al menú principal...")

        elif opcion == "3":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            try:
                eliminar_estudiante()
            except SalirOperacion:
                print(" Regresando al menú principal...")

        elif opcion == "4":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            mostrar_lista()

        elif opcion == "5":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            try:
                generar_pdf()
            except SalirOperacion:
                print(" Regresando al menú principal...")

        elif opcion == "6":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print(" Regresando al menú principal...")
                continue
            mostrar_historial()

        elif opcion == "7":
            op = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ").strip().lower()
            if op == "salir":
                print("↩ Regresando al menú principal...")
                continue
            mostrar_pendientes()

        else:
            print(" Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
