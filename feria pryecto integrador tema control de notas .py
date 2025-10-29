import re
from datetime import datetime
from Anime import animacion, Fore, Style, init  
from Generador import generar


estudiantes = []

def pedir_dato_confirmar(prompt, tipo=str, validar=None, ejemplo=None, mayus=False, obligatorio=True):
    while True:
        raw = input(f"   → {prompt}: ").strip()
        if raw.lower() == "salir":
            raise KeyboardInterrupt

        if obligatorio and raw == "":
            print("⚠️ Este campo no puede quedar vacío.")
            continue

        try:
            if tipo == int:
                valor = int(raw)
            elif tipo == float:
                valor = float(raw)
            else:
                valor = raw.upper() if mayus else raw
        except ValueError:
            print("⚠️ Tipo de dato incorrecto. Intenta de nuevo.")
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
                print(f"⚠️ {msg}")
                continue

        while True:
            print(f"   ✅ Has ingresado: {valor}")
            print("   ¿Deseas confirmar este dato?")
            print("   1. Confirmar")
            print("   2. Modificar")
            opcion = input("   Elige (1-2): ").strip()
            if opcion == "1":
                return valor
            elif opcion == "2":
                print("   🔁 Volvamos a ingresarlo...")
                break
            else:
                print("⚠️ Debes ingresar 1 o 2. Intenta de nuevo.")

def confirmar_si_no(prompt):
    r = input(f"{prompt} (S = sí / cualquier otra tecla = no): ").strip().upper()
    return r == "S"


def calcular_promedio(lista_notas):
    if not lista_notas:
        return 0.0
    return round(sum(lista_notas) / len(lista_notas), 2)

def agregar_estudiante():
    try:
        print("\n" + "="*70)
        print("📌 REGISTRO DE NUEVOS ESTUDIANTES")
        print("="*70)

        while True:
            try:
                cantidad_estudiantes = pedir_dato_confirmar(
                    "¿Cuántos estudiantes deseas agregar?",
                    tipo=int,
                    validar=lambda x: x > 0,
                    ejemplo="1",
                )
                break
            except KeyboardInterrupt:
                print("\n↩️ Operación cancelada. Regresando al menú principal...")
                return

        for i in range(1, cantidad_estudiantes + 1):
            print("\n" + "-"*60)
            print(f"🧑‍🎓 Estudiante {i}")
            print("-"*60)

            nombre = pedir_dato_confirmar("Nombre", str, mayus=True)
            apellido = pedir_dato_confirmar("Apellido", str, mayus=True)

            cedula = pedir_dato_confirmar(
                "Cédula (000-000000-0000A)",
                str,
                validar=lambda v: bool(re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", v)),
                ejemplo="001-123456-0000A",
                mayus=True
            )

            carnet = pedir_dato_confirmar(
                "Carnet (25-00000-0)",
                str,
                validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)),
                ejemplo="25-02365-9"
            )

            municipio = pedir_dato_confirmar("Municipio", str, mayus=True)
            departamento = pedir_dato_confirmar("Departamento", str, mayus=True)

            edad = pedir_dato_confirmar("Edad", int, validar=lambda x: 10 <= x <= 120, ejemplo="20")

            while True:
                try:
                    op_gen = pedir_dato_confirmar("Género (1. Masculino / 2. Femenino)", str,
                                                  validar=lambda s: s in ["1", "2"])
                    genero = "Masculino" if op_gen == "1" else "Femenino"
                    break
                except KeyboardInterrupt:
                    raise

            tipo_sangre = pedir_dato_confirmar(
               "Tipo de sangre (A+, A-, B+, B-, AB+, AB-, O+, O-)",
                str,
                validar=lambda v: bool(re.fullmatch(r"^(A|B|AB|O)[+-]$", v.upper())),
                ejemplo="O+"
            )

            modalidad_op = pedir_dato_confirmar(
                "Modalidad (1. Presencial / 2. Virtual / 3. Mixta)",
                str,
                validar=lambda s: s in ["1", "2", "3"]
            )
            modalidad = {"1": "Presencial", "2": "Virtual", "3": "Mixta"}[modalidad_op]

            situacion_op = pedir_dato_confirmar(
                "Situación académica (1. Regular / 2. Sabatino / 3. Dominical)",
                str,
                validar=lambda s: s in ["1", "2", "3"]
            )
            situacion = {"1": "Regular", "2": "Sabatino", "3": "Dominical"}[situacion_op]

            carrera = pedir_dato_confirmar("Carrera", str, mayus=True)

            anio = pedir_dato_confirmar("Año actual (1-6)", int, validar=lambda x: 1 <= x <= 6, ejemplo="1")

            ciclo = pedir_dato_confirmar("Ciclo actual (1–11)", int, validar=lambda x: 1 <= x <= 11, ejemplo="1")
            semestre = pedir_dato_confirmar("Semestre (1 o 2)", int, validar=lambda x: x in [1,2], ejemplo="1")

            area = pedir_dato_confirmar("Área de conocimiento", str, mayus=True)

            idiomas_cant = pedir_dato_confirmar("¿Cuántos idiomas domina? (mínimo 1)", int,
                                                validar=lambda x: x >= 1, ejemplo="1")
            idiomas = []
            for idx in range(1, idiomas_cant + 1):
                idi = pedir_dato_confirmar(f"Idioma {idx}", str, mayus=True)
                idiomas.append(idi)

            materias_cant = pedir_dato_confirmar("¿Cuántas materias cursa este estudiante?", int,
                                                 validar=lambda x: x > 0, ejemplo="2")
            materias = []
            for m in range(1, materias_cant + 1):
                print("\n" + "-"*40)
                print(f"📘 Materia {m}")
                nombre_mat = pedir_dato_confirmar(f"Nombre de la materia {m}", str, mayus=True)

                print("📖 Ingresando notas para la materia: (C1P1, C1P2, C2P1, C2P2)")
                notas = {}
                for ciclo_n in (1, 2):
                    for parcial_n in (1, 2):
                        key = f"C{ciclo_n}P{parcial_n}"
                        valor = pedir_dato_confirmar(
                            f"Ciclo {ciclo_n} - Parcial {parcial_n} (0-100)",
                            float,
                            validar=lambda x: 0 <= x <= 100,
                            ejemplo="88"
                        )
                        notas[key] = valor

                # calcular promedio por materia y estado
                valores = [v for v in notas.values() if isinstance(v, (int, float, float))]
                promedio_mat = calcular_promedio(valores)
                estado_mat = "Aprobado" if promedio_mat >= 60 else "Reprobado"

                materias.append({
                    "materia": nombre_mat,
                    "notas": notas,
                    "promedio": promedio_mat,
                    "estado": estado_mat
                })
                print(f"   ➤ Promedio final de {nombre_mat}: {promedio_mat:.2f} | Estado: {estado_mat}")

            print("\n" + "="*60)
            print("🧾 RESUMEN DEL ESTUDIANTE")
            print("="*60)
            nombre_completo = f"{nombre} {apellido}"
            print(f"👤 {nombre_completo}")
            print(f"🪪 Cédula: {cedula} | 🎟 Carnet: {carnet}")
            print(f"🎓 Carrera: {carrera} | Año: {anio} | Ciclo: {ciclo} | Semestre: {semestre}")
            print(f"📚 Materias registradas: {len(materias)}")
            for mat in materias:
                print(f"   - {mat['materia']}: Promedio {mat['promedio']:.2f} | {mat['estado']}")
            promedio_general = calcular_promedio([m["promedio"] for m in materias])
            estado_final = "Aprobado" if promedio_general >= 60 else "Reprobado"
            print("-"*60)
            print(f"📊 Índice Académico (Promedio general): {promedio_general:.2f}")
            print(f"🎯 Estado final del año: {estado_final}")
            print("="*60)

            confirmar = confirmar_si_no("¿Deseas confirmar y guardar este estudiante?")
            if not confirmar:
                print("❌ Registro cancelado. No se guardaron los datos.")
                continue

            fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            estudiante = {
                "nombre": nombre,
                "apellido": apellido,
                "cedula": cedula,
                "carnet": carnet,
                "municipio": municipio,
                "departamento": departamento,
                "edad": edad,
                "genero": genero,
                "sangre": tipo_sangre,
                "modalidad": modalidad,
                "situacion": situacion,
                "carrera": carrera,
                "anio": anio,
                "ciclo": ciclo,
                "semestre": semestre,
                "area": area,
                "idiomas": idiomas,
                "materias": materias,
                "promedio": promedio_general,
                "fecha_registro": fecha_registro,
                "ultima_modificacion": None
            }

            estudiantes.append(estudiante)
            print("\n✅ Estudiante agregado correctamente.")
            print(f"📅 Fecha de registro: {fecha_registro}")
            print("-"*70)

    except KeyboardInterrupt:
        print("\n⚠️ Registro cancelado por el usuario. Regresando al menú principal...")

def mostrar_lista():
    if not estudiantes:
        print("⚠️ No hay estudiantes registrados.")
        return

    print("\n" + "="*60)
    print("📋 LISTA COMPLETA DE ESTUDIANTES")
    print("="*60)
    for idx, est in enumerate(estudiantes, start=1):
        print("\n" + "-"*60)
        print(f"#{idx}  👤 {est['nombre']} {est['apellido']}  |  🎟 Carnet: {est['carnet']}")
        print(f"📍 {est['municipio']}, {est['departamento']}  |  🎓 {est['carrera']} (Año {est['anio']}, Ciclo {est['ciclo']})")
        print(f"🗣 Idiomas: {', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
        print("📘 MATERIAS Y NOTAS:")
        for m in est['materias']:
            notas = m['notas']
            print(f"  • {m['materia']}: C1P1={notas.get('C1P1','')} C1P2={notas.get('C1P2','')} C2P1={notas.get('C2P1','')} C2P2={notas.get('C2P2','')} -> Prom: {m['promedio']:.2f} | {m['estado']}")
        print(f"📊 Índice Académico: {est.get('promedio',0):.2f}  |  Estado final: {'Aprobado ✅' if est.get('promedio',0)>=60 else 'Reprobado ❌'}")
        print(f"✉️ Registrado el: {est.get('fecha_registro')}  |  Última modif.: {est.get('ultima_modificacion')}")
        print("-"*60)


# Buscar estudiante por carnet (y opciones: ver / editar / eliminar)

def buscar_estudiante():
    try:
        carnet = pedir_dato_confirmar("Ingrese el carnet a buscar (25-00000-0)", str,
                                      validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)),
                                      ejemplo="25-02365-9")
        # buscar
        for est in estudiantes:
            if est["carnet"] == carnet:
                # Mostrar detalle
                print("\n" + "="*50)
                print(f"👤 {est['nombre']} {est['apellido']}  |  🎟 {est['carnet']}")
                print("="*50)
                print(f"🪪 Cédula: {est['cedula']}")
                print(f"📍 {est['municipio']} - {est['departamento']}")
                print(f"🎂 Edad: {est['edad']} | Género: {est['genero']} | Sangre: {est['sangre']}")
                print(f"🎓 Carrera: {est['carrera']} | Año: {est['anio']} | Ciclo: {est['ciclo']} | Semestre: {est['semestre']}")
                print(f"🏫 Modalidad: {est['modalidad']} | Situación: {est['situacion']}")
                print(f"📚 Área: {est['area']}")
                print(f"🗣 Idiomas: {', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
                print("📘 MATERIAS:")
                for m in est['materias']:
                    notas = m['notas']
                    print(f"  • {m['materia']}: C1P1={notas.get('C1P1','')} C1P2={notas.get('C1P2','')} C2P1={notas.get('C2P1','')} C2P2={notas.get('C2P2','')} -> Prom: {m['promedio']:.2f} | {m['estado']}")
                print(f"📊 Índice Académico: {est.get('promedio',0):.2f} | Estado final: {'Aprobado ✅' if est.get('promedio',0)>=60 else 'Reprobado ❌'}")
                print(f"📅 Registrado: {est.get('fecha_registro')}  |  Última modificación: {est.get('ultima_modificacion')}")
                print("="*50)

                while True:
                    print("\n¿Qué deseas hacer con este registro?")
                    print("1. Editar datos")
                    print("2. Eliminar estudiante")
                    print("3. Volver al menú")
                    op = input("Elige (1-3): ").strip()
                    if op == "1":
                        editar_estudiante(est)
                        break
                    elif op == "2":
                        eliminar_estudiante(carnet)
                        break
                    elif op == "3":
                        return
                    else:
                        print("⚠️ Opción inválida. Usa 1, 2 o 3.")
                return
        print("⚠️ Estudiante no encontrado.")
    except KeyboardInterrupt:
        print("\n↩️ Búsqueda cancelada. Regresando al menú principal...")


# Eliminar estudiante (por carnet)
def eliminar_estudiante(carnet=None):
    try:
        if not carnet:
            carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante a eliminar (25-00000-0)", str,
                                          validar=lambda v: bool(re.fullmatch(r"25-\d{5}-\d", v)),
                                          ejemplo="25-02365-9")
        for i, est in enumerate(estudiantes):
            if est["carnet"] == carnet:
                confirmar = confirmar_si_no(f"¿Seguro que deseas eliminar a {est['nombre']} {est['apellido']}?")
                if confirmar:
                    del estudiantes[i]
                    print("🗑 Estudiante eliminado correctamente.")
                else:
                    print("↩️ Operación cancelada. No se eliminó.")
                return
        print("⚠️ Estudiante no encontrado.")
    except KeyboardInterrupt:
        print("\n↩️ Eliminación cancelada. Regresando al menú...")


def editar_estudiante(est):
    try:
        while True:
            print("\n" + "-"*50)
            print(f"✏️ Editando: {est['nombre']} {est['apellido']}  |  Carnet: {est['carnet']}")
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
            print("15. Semestre")
            print("16. Área de conocimiento")
            print("17. Idiomas")
            print("18. Materias (agregar/quitar)")
            print("19. Editar notas de una materia")
            print("20. Volver")
            opc = input("Elige (1-20): ").strip()
            if opc == "1":
                nuevo = pedir_dato_confirmar("Nuevo nombre", str, mayus=True)
                est["nombre"] = nuevo
                print("✅ Nombre actualizado.")
            elif opc == "2":
                nuevo = pedir_dato_confirmar("Nuevo apellido", str, mayus=True)
                est["apellido"] = nuevo
                print("✅ Apellido actualizado.")
            elif opc == "3":
                nuevo = pedir_dato_confirmar("Nueva cédula (000-000000-0000A)", str,
                                             validar=lambda v: bool(re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", v)),
                                             ejemplo="001-123456-0000A",
                                             mayus=True)
                est["cedula"] = nuevo
                print("✅ Cédula actualizada.")
            elif opc == "4":
                while True:
                    nuevo = pedir_dato_confirmar("Nuevo carnet (25-00000-0)", str,
                                                 validar=lambda v: bool(re.fullmatch(r"25-\d{5}-\d", v)),
                                                 ejemplo="25-02365-9")
                    # verificar unicidad
                    if any(e["carnet"] == nuevo and e is not est for e in estudiantes):
                        print("⚠️ Ya existe otro estudiante con ese carnet. Intenta otro.")
                    else:
                        est["carnet"] = nuevo
                        print("✅ Carnet actualizado.")
                        break
            elif opc == "5":
                nuevo = pedir_dato_confirmar("Nuevo municipio", str, mayus=True)
                est["municipio"] = nuevo
                print("✅ Municipio actualizado.")
            elif opc == "6":
                nuevo = pedir_dato_confirmar("Nuevo departamento", str, mayus=True)
                est["departamento"] = nuevo
                print("✅ Departamento actualizado.")
            elif opc == "7":
                nuevo = pedir_dato_confirmar("Nueva edad", int, validar=lambda x: 10 <= x <= 120, ejemplo="20")
                est["edad"] = nuevo
                print("✅ Edad actualizada.")
            elif opc == "8":
                nuevo = pedir_dato_confirmar("Género (1. Masculino / 2. Femenino)", str, validar=lambda s: s in ["1","2"])
                est["genero"] = "Masculino" if nuevo == "1" else "Femenino"
                print("✅ Género actualizado.")
            elif opc == "9":
                nuevo = pedir_dato_confirmar("Nuevo tipo de sangre (A+, O-, AB-, ...)", str,
                                             validar=lambda v: bool(re.fullmatch(r"(A|B|AB|O)[+-]", v)),
                                             mayus=True)
                est["sangre"] = nuevo
                print("✅ Tipo de sangre actualizado.")
            elif opc == "10":
                op = pedir_dato_confirmar("Modalidad (1. Presencial / 2. Virtual / 3. Mixta)", str,
                                          validar=lambda s: s in ["1","2","3"])
                est["modalidad"] = {"1": "Presencial", "2": "Virtual", "3": "Mixta"}[op]
                print("✅ Modalidad actualizada.")
            elif opc == "11":
                op = pedir_dato_confirmar("Situación académica (1. Regular / 2. Sabatino / 3. Dominical)", str,
                                          validar=lambda s: s in ["1","2","3"])
                est["situacion"] = {"1": "Regular", "2": "Sabatino", "3": "Dominical"}[op]
                print("✅ Situación actualizada.")
            elif opc == "12":
                nuevo = pedir_dato_confirmar("Nueva carrera", str, mayus=True)
                est["carrera"] = nuevo
                print("✅ Carrera actualizada.")
            elif opc == "13":
                nuevo = pedir_dato_confirmar("Nuevo año (1-6)", int, validar=lambda x: 1 <= x <= 6)
                est["anio"] = nuevo
                print("✅ Año actualizado.")
            elif opc == "14":
                nuevo = pedir_dato_confirmar("Nuevo ciclo (1–11)", int, validar=lambda x: 1 <= x <= 11)
                est["ciclo"] = nuevo
                print("✅ Ciclo actualizado.")
            elif opc == "15":
                nuevo = pedir_dato_confirmar("Nuevo semestre (1 o 2)", int, validar=lambda x: x in [1,2])
                est["semestre"] = nuevo
                print("✅ Semestre actualizado.")
            elif opc == "16":
                nuevo = pedir_dato_confirmar("Nueva área de conocimiento", str, mayus=True)
                est["area"] = nuevo
                print("✅ Área actualizada.")
            elif opc == "17":
                cant = pedir_dato_confirmar("¿Cuántos idiomas ahora?", int, validar=lambda x: x>=0)
                idiomas = []
                for j in range(1, cant+1):
                    idi = pedir_dato_confirmar(f"Idioma {j}", str, mayus=True)
                    idiomas.append(idi)
                est["idiomas"] = idiomas
                print("✅ Idiomas actualizados.")
            elif opc == "18":
                # Agregar o quitar materias
                print("1. Agregar materia")
                print("2. Quitar materia")
                opm = input("Elige (1-2): ").strip()
                if opm == "1":
                    nombre_n = pedir_dato_confirmar("Nombre de la nueva materia", str, mayus=True)
                    notas = {}
                    print("Ingresa las 4 notas de la materia nueva:")
                    for c in (1,2):
                        for p in (1,2):
                            key = f"C{c}P{p}"
                            val = pedir_dato_confirmar(f"C{c}P{p} (0-100)", float, validar=lambda x: 0<=x<=100)
                            notas[key] = val
                    prom = calcular_promedio(list(notas.values()))
                    estado = "Aprobado" if prom >= 60 else "Reprobado"
                    est['materias'].append({"materia": nombre_n, "notas": notas, "promedio": prom, "estado": estado})
                    print("✅ Materia agregada.")
                elif opm == "2":
                    # listar materias
                    if not est['materias']:
                        print("⚠️ No hay materias para quitar.")
                    else:
                        print("Materias actuales:")
                        for idx, m in enumerate(est['materias'], start=1):
                            print(f"{idx}. {m['materia']}")
                        try:
                            sel = int(input("Seleccione el número de la materia a quitar: ").strip())
                            if 1 <= sel <= len(est['materias']):
                                borr = est['materias'].pop(sel-1)
                                print(f"🗑 Materia {borr['materia']} eliminada.")
                            else:
                                print("⚠️ Selección inválida.")
                        except ValueError:
                            print("⚠️ Ingresa un número válido.")
                else:
                    print("⚠️ Opción inválida.")
            elif opc == "19":
                if not est['materias']:
                    print("⚠️ No hay materias para editar.")
                else:
                    print("Materias:")
                    for idx, m in enumerate(est['materias'], start=1):
                        print(f"{idx}. {m['materia']}")
                    try:
                        sel = int(input("Selecciona materia a editar (número): ").strip())
                        if 1 <= sel <= len(est['materias']):
                            mobj = est['materias'][sel-1]
                            notas = mobj['notas']
                            print(f"Editando notas de {mobj['materia']}")
                            for c in (1,2):
                                for p in (1,2):
                                    key = f"C{c}P{p}"
                                    newval = pedir_dato_confirmar(f"Nueva nota {key} (0-100)", float, validar=lambda x: 0<=x<=100)
                                    notas[key] = newval
                            mobj['promedio'] = calcular_promedio([v for v in notas.values()])
                            mobj['estado'] = "Aprobado" if mobj['promedio'] >= 60 else "Reprobado"
                            print("✅ Notas actualizadas.")
                        else:
                            print("⚠️ Selección inválida.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif opc == "20":
                est['ultima_modificacion'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("↩️ Volviendo al menú anterior...")
                break
            else:
                print("⚠️ Opción inválida. Intente de nuevo.")

            est['ultima_modificacion'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    except KeyboardInterrupt:
        print("\n↩️ Edición cancelada. Regresando al menú...")

def generar_pdf():
    if not estudiantes:
        print("⚠️ No hay estudiantes registrados.")
        return
    try:
        carnet = pedir_dato_confirmar("Ingrese el carnet del estudiante para generar su certificado (25-00000-0)", str,
                                      validar=lambda v: bool(re.fullmatch(r"\d{2}-\d{5}-\d", v)),
                                      ejemplo="25-02365-9")
        encontrado = None
        for est in estudiantes:
            if est['carnet'] == carnet:
                encontrado = est
                break
        if not encontrado:
            print(f"⚠️ No se encontró al estudiante con carnet {carnet}.")
            return
        nombre_pdf = f"certificado_{encontrado['carnet'].replace('-', '_')}.pdf"
        generar(encontrado, nombre_pdf)
    except KeyboardInterrupt:
        print("\n↩️ Operación cancelada. Regresando al menú...")


def mostrar_menu():
    print("\n" + "="*50)
    print("🎓 MENÚ PRINCIPAL")
    print("="*50)
    print("1. Agregar estudiante")
    print("2. Buscar / Ver / Editar estudiante (por carnet)")
    print("3. Eliminar estudiante (por carnet)")
    print("4. Mostrar lista de estudiantes")
    print("5. Generar certificados PDF")
    print("6. Salir")

def main():
    print("=" * 60)
    print("✨ Bienvenido al Sistema de Control de Notas ✨")
    print("=" * 60)
    try:
        animacion()
    except Exception:
        pass
    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción (1-6): ").strip()
            if opcion == "1":
                try:
                    aviso = "   Para cancelar la operación y volver al menú, escribe 'salir'.\n   Presiona Enter para continuar..."
                    _ = input(aviso)
                    agregar_estudiante()
                except KeyboardInterrupt:
                    pass
            elif opcion == "2":
                try:
                    _ = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ")
                    buscar_estudiante()
                except KeyboardInterrupt:
                    pass
            elif opcion == "3":
                try:
                    _ = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ")
                    eliminar_estudiante()
                except KeyboardInterrupt:
                    pass
            elif opcion == "4":
                _ = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ")
                mostrar_lista()
            elif opcion == "5":
                try:
                    _ = input("   Presiona Enter para continuar (o escribe 'salir' para volver): ")
                    generar_pdf()
                except KeyboardInterrupt:
                    pass
            elif opcion == "6":
                print("👋 Gracias por usar el sistema. ¡Hasta pronto!")
                break
            else:
                print("⚠️ Opción inválida. Intente de nuevo.")
        except Exception as e:
            print(f"⚠️ Error inesperado en el menú: {e}")

if __name__ == "__main__":
    main()
