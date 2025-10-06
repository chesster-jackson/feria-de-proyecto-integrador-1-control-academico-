import re
from datetime import datetime

estudiantes = []

def calcular_promedio(notas):
    return sum(notas) / len(notas) if notas else 0.0

# -------------------------------
# Función para agregar estudiante
# -------------------------------
def agregar_estudiante(estudiantes):
    print("="*50)
    print("📌 Registro de nuevos estudiantes")
    print("="*50)

    while True:
        try:
            cantidad_estudiantes = int(input("¿Cuántos estudiantes deseas agregar?: ").strip())
            if cantidad_estudiantes > 0:
                break
            else:
                print("⚠️ Debes ingresar un número positivo.")
        except ValueError:
            print("⚠️ Valor inválido. Intenta de nuevo.")

    for i in range(cantidad_estudiantes):
        print("\n" + "-"*50)
        print(f"🧑‍🎓 Estudiante {i+1}")
        print("-"*50)

        # Nombre
        while True:
            nombre = input("Nombre: ").strip()
            if nombre:
                break
            print("⚠️ El nombre no puede estar vacío.")

        # Apellido
        while True:
            apellido = input("Apellido: ").strip()
            if apellido:
                break
            print("⚠️ El apellido no puede estar vacío.")

        # Cédula (formato 000-000000-0000A)
        while True:
            cedula = input("Cédula (formato 000-000000-0000A): ").strip().upper()
            if not cedula:
                print("⚠️ La cédula no puede estar vacía.")
            elif not re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", cedula):
                print("⚠️ Formato inválido. Ejemplo: 001-123456-0000a")
            else:
                break

        # Carnet
        while True:
            carnet = input("Número de carnet (formato 25-00000-0): ").strip()
            if not carnet:
                print("⚠️ El carnet no puede estar vacío.")
            elif any(est["carnet"] == carnet for est in estudiantes):
                print("⚠️ Ya existe un estudiante con ese carnet.")
            elif not re.fullmatch(r"\d{2}-\d{5}-\d", carnet):
                print("⚠️ Formato inválido. Ejemplo correcto: 25-0000-0")
            else:
                break

        # Municipio
        while True:
            municipio = input("Municipio: ").strip()
            if municipio:
                break
            print("⚠️ El municipio no puede estar vacío.")

        # Departamento
        while True:
            departamento = input("Departamento: ").strip()
            if departamento:
                break
            print("⚠️ El departamento no puede estar vacío.")

        # Edad
        while True:
            try:
                edad = int(input("Edad: ").strip())
                if edad > 0:
                    break
                else:
                    print("⚠️ La edad debe ser positiva.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Género (selección numérica)
        while True:
            try:
                print("\nGénero:")
                print("1. Masculino")
                print("2. Femenino")
                op = int(input("Elige (1-2): ").strip())
                if op == 1:
                    genero = "M"
                    break
                elif op == 2:
                    genero = "F"
                    break
                else:
                    print("⚠️ Opción inválida.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Sangre
        while True:
            sangre = input("Tipo de sangre (ej: A+, O-, B+): ").strip().upper()
            if sangre:
                break
            print("⚠️ El tipo de sangre no puede estar vacío.")

        # Modalidad (selección numérica)
        while True:
            try:
                print("\nModalidad:")
                print("1. Presencial")
                print("2. Virtual")
                print("3. Mixta")
                op = int(input("Elige (1-3): ").strip())
                if op == 1:
                    modalidad = "Presencial"
                    break
                elif op == 2:
                    modalidad = "Virtual"
                    break
                elif op == 3:
                    modalidad = "Mixta"
                    break
                else:
                    print("⚠️ Opción inválida.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Situación académica (selección numérica)
        while True:
            try:
                print("\nSituación académica:")
                print("1. Regular")
                print("2. Sabatino")
                print("3. Dominical")
                op = int(input("Elige (1-3): ").strip())
                if op == 1:
                    situacion = "Regular"
                    break
                elif op == 2:
                    situacion = "Sabatino"
                    break
                elif op == 3:
                    situacion = "Dominical"
                    break
                else:
                    print("⚠️ Opción inválida.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Carrera
        while True:
            carrera = input("Nombre de la carrera: ").strip()
            if carrera:
                break
            print("⚠️ La carrera no puede estar vacía.")

        # Año (anio)
        while True:
            try:
                anio = int(input("Año actual ( 1,2,3,...6 ): ").strip())
                if 1 <= anio <= 6:
                    break
                else:
                    print("⚠️ El año debe rondar de 1 al 6.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Ciclo
        while True:
            try:
                ciclo = int(input("Ciclo (1 o 2): ").strip())
                if ciclo in [1, 2]:
                    break
                else:
                    print("⚠️ Solo puede ser 1 o 2.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Semestre
        while True:
            try:
                semestre = int(input("Semestre (1 o 2): ").strip())
                if semestre in [1, 2]:
                    break
                else:
                    print("⚠️ Solo puede ser 1 o 2.")
            except ValueError:
                print("⚠️ Ingresa un número válido.")

        # Área de conocimiento
        while True:
            area = input("Área de conocimiento: ").strip()
            if area:
                break
            print("⚠️ El área de conocimiento no puede estar vacía.")

        # Idiomas
        idiomas = []
        while True:
            try:
                cantidad_idiomas = int(input("¿Cuántos idiomas domina?: ").strip())
                if cantidad_idiomas >= 0:
                    break
                else:
                    print("⚠️ Debe ser cero o un número positivo.")
            except ValueError:
                print("⚠️ Número inválido.")

        for j in range(cantidad_idiomas):
            while True:
                idioma = input(f" - Idioma {j+1}: ").strip()
                if idioma:
                    idiomas.append(idioma)
                    break
                print("⚠️ El idioma no puede estar vacío.")

        # Materia
        while True:
            materia = input("Materia : ").strip()
            if materia:
                break
            print("⚠️ La materia no puede estar vacía.")

        # Notas (4 parciales)
        notas = []
        print("📖 Ingrese las notas de los 4 parciales (0-100):")
        for p in range(1, 5):
            while True:
                try:
                    nota = float(input(f" Parcial {p}: ").strip())
                    if 0 <= nota <= 100:
                        notas.append(nota)
                        break
                    else:
                        print("⚠️ La nota debe estar entre 0 y 100.")
                except ValueError:
                    print("⚠️ Ingresa un número válido.")

        promedio = calcular_promedio(notas)

        # Fecha de registro
        fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        estudiantes.append({
            "nombre": nombre,
            "apellido": apellido,
            "cedula": cedula,
            "carnet": carnet,
            "municipio": municipio,
            "departamento": departamento,
            "edad": edad,
            "genero": genero,
            "sangre": sangre,
            "modalidad": modalidad,
            "situacion": situacion,
            "carrera": carrera,
            "anio": anio,
            "ciclo": ciclo,
            "semestre": semestre,
            "area": area,
            "idiomas": idiomas,
            "materia": materia,
            "notas": notas,
            "promedio": promedio,
            "fecha_registro": fecha_registro,
            "ultima_modificacion": None
        })
        print("✅ Estudiante agregado correctamente.")

# -------------------------------
# Mostrar lista completa
# -------------------------------
def mostrar_lista(estudiantes):
    if not estudiantes:
        print("⚠️ No hay estudiantes registrados.")
        return

    print("="*50)
    print("📋 Lista completa de estudiantes")
    print("="*50)

    for est in estudiantes:
        estado = "Aprobado ✅" if est["promedio"] >= 60 else "Reprobado ❌"
        print("\n" + "-"*50)
        print(f"👤 Nombre completo: {est['nombre']} {est['apellido']}")
        print(f"🪪 Cédula: {est['cedula']}")
        print(f"🎟 Carnet: {est['carnet']}")
        print(f"📍 Municipio: {est['municipio']} | Departamento: {est['departamento']}")
        print(f"🎂 Edad: {est['edad']} | Género: {est['genero']} | Sangre: {est['sangre']}")
        print(f"🎓 Carrera: {est['carrera']} | Año: {est['anio']} | Ciclo: {est['ciclo']} | Semestre: {est['semestre']}")
        print(f"🏫 Modalidad: {est['modalidad']} | Situación académica: {est['situacion']}")
        print(f"📚 Área de conocimiento: {est['area']}")
        print(f"🗣 Idiomas: {', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
        print(f"📘 Materia inscrita: {est['materia']}")
        # Mostrar nota por parcial y promedio
        for idx, n in enumerate(est['notas'], start=1):
            print(f"   - Parcial {idx}: {n:.2f}")
        print(f"   -> Promedio: {est['promedio']:.2f} | Estado: { 'Aprobado ✅' if est['promedio'] >= 60 else 'Reprobado ❌'}")
        print(f"📅 Fecha de registro: {est['fecha_registro']}")
        if est.get("ultima_modificacion"):
            print(f"✏️ Última modificación: {est['ultima_modificacion']}")
        print("-"*50)

# -------------------------------
# Buscar estudiante (y opción editar/eliminar)
# -------------------------------
def buscar_estudiante(estudiantes):
    try:
        carnet = input("Ingrese el carnet a buscar (formato 25-0000-0): ").strip()
        if not re.fullmatch(r"\d{2}-\d{5}-\d", carnet):
            print("⚠️ Formato inválido. Ejemplo: 25-0000-0")
            return
        for est in estudiantes:
            if est["carnet"] == carnet:
                # Mostrar detalles (como en mostrar_lista pero solo de este estudiante)
                print("="*50)
                print(f"👤 {est['nombre']} {est['apellido']} ({est['carnet']})")
                print(f"🪪 Cédula: {est['cedula']}")
                print(f"📍 {est['municipio']} - {est['departamento']}")
                print(f"🎂 {est['edad']} años | Género: {est['genero']} | Sangre: {est['sangre']}")
                print(f"🎓 Carrera: {est['carrera']} | Año: {est['anio']} | Ciclo: {est['ciclo']} | Semestre: {est['semestre']}")
                print(f"🏫 Modalidad: {est['modalidad']} | Situación: {est['situacion']}")
                print(f"📚 Área: {est['area']}")
                print(f"🗣 Idiomas: {', '.join(est['idiomas']) if est['idiomas'] else 'Ninguno'}")
                print(f"📘 Materia: {est['materia']}")
                for idx, n in enumerate(est['notas'], start=1):
                    print(f"   - Parcial {idx}: {n:.2f}")
                print(f"   -> Promedio: {est['promedio']:.2f}")
                estado = "Aprobado ✅" if est["promedio"] >= 60 else "Reprobado ❌"
                print(f"Estado final: {estado}")
                print(f"📅 Registrado el: {est['fecha_registro']}")
                if est.get("ultima_modificacion"):
                    print(f"✏️ Última modificación: {est['ultima_modificacion']}")
                print("="*50)

                # Opciones post-búsqueda
                while True:
                    try:
                        print("\n¿Qué deseas hacer con este registro?")
                        print("1. Editar datos")
                        print("2. Eliminar estudiante")
                        print("3. Volver al menú")
                        op = int(input("Elige (1-3): ").strip())
                        if op == 1:
                            editar_estudiante(estudiantes, est)
                            break
                        elif op == 2:
                            eliminar_estudiante(estudiantes, carnet_confirm=carnet)
                            break
                        elif op == 3:
                            return
                        else:
                            print("⚠️ Opción inválida.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
                return
        print("⚠️ Estudiante no encontrado.")
    except Exception as e:
        print(f"⚠️ Error en búsqueda: {e}")

# -------------------------------
# Eliminar estudiante
# -------------------------------
def eliminar_estudiante(estudiantes, carnet_confirm=None):
    try:
        if carnet_confirm:
            carnet = carnet_confirm
        else:
            carnet = input("Ingrese el carnet del estudiante a eliminar (formato 25-0000-0): ").strip()
        if not re.fullmatch(r"\d{2}-\d{5}-\d", carnet):
            print("⚠️ Formato inválido. Ejemplo: 25-0000-0")
            return
        for i, est in enumerate(estudiantes):
            if est["carnet"] == carnet:
                # confirmación
                confirm = input(f"¿Seguro que deseas eliminar al estudiante llamado {est['nombre']} {est['apellido']}? (s/n): ").strip().lower()
                if confirm == "s":
                    del estudiantes[i]
                    print("🗑 Estudiante eliminado correctamente.")
                else:
                    print("Operación cancelada.")
                return
        print("⚠️ Estudiante no encontrado.")
    except Exception as e:
        print(f"⚠️ Error al eliminar: {e}")

# -------------------------------
# Editar estudiante (por campos)
# -------------------------------
def editar_estudiante(estudiantes, est):
    try:
        while True:
            print(f"\n¿Qué campo deseas editar del estudiante llamado {est['nombre']} {est['apellido']} y con número de carnet {est['carnet']}?")
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
            print("18. Materia")
            print("19. Notas (4 parciales)")
            print("20. Volver")
            try:
                op = int(input("Elige (1-20): ").strip())
            except ValueError:
                print("⚠️ Ingresa un número válido.")
                continue

            if op == 1:
                print("¿Confirmas que quieres hacer esta acción? (s/n)")
                confirmar = input().strip().lower()
                if confirmar == "s":
                    nuevo = input("Nuevo nombre: ").strip()
                    if nuevo:
                        est["nombre"] = nuevo
                        print("✅ Nombre actualizado.")
                    else:
                        print("⚠️ saliento del programa.")
                        break
            elif op == 2:
                nuevo = input("Nuevo apellido: ").strip()
                if nuevo:
                    est["apellido"] = nuevo
                    print("✅ Apellido actualizado.")
                else:
                    print("⚠️ Apellido vacío, no se modificó.")
            elif op == 3:
                while True:
                    nuevo = input("Nueva cédula (formato 000-000000-0000A): ").strip().upper()
                    if not nuevo:
                        print("⚠️ La cédula no puede estar vacía.")
                    elif not re.fullmatch(r"\d{3}-\d{6}-\d{4}[A-Z]", nuevo):
                        print("⚠️ Formato inválido.")
                    else:
                        est["cedula"] = nuevo
                        print("✅ Cédula actualizada.")
                        break
            elif op == 4:
                while True:
                    nuevo = input("Nuevo carnet (formato 25-0000-0): ").strip()
                    if not nuevo:
                        print("⚠️ El carnet no puede estar vacío.")
                    elif any(e["carnet"] == nuevo and e is not est for e in estudiantes):
                        print("⚠️ Ya existe otro estudiante con ese carnet.")
                    elif not re.fullmatch(r"\d{2}-\d{4}-\d", nuevo):
                        print("⚠️ Formato inválido.")
                    else:
                        est["carnet"] = nuevo
                        print("✅ Carnet actualizado.")
                        break
            elif op == 5:
                nuevo = input("Nuevo municipio: ").strip()
                if nuevo:
                    est["municipio"] = nuevo
                    print("✅ Municipio actualizado.")
                else:
                    print("⚠️ Municipio vacío, no se modificó.")
            elif op == 6:
                nuevo = input("Nuevo departamento: ").strip()
                if nuevo:
                    est["departamento"] = nuevo
                    print("✅ Departamento actualizado.")
                else:
                    print("⚠️ Departamento vacío, no se modificó.")
            elif op == 7:
                while True:
                    try:
                        nuevo = int(input("Nueva edad: ").strip())
                        if nuevo > 0:
                            est["edad"] = nuevo
                            print("✅ Edad actualizada.")
                            break
                        else:
                            print("⚠️ La edad debe ser positiva.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif op == 8:
                while True:
                    try:
                        print("Género:")
                        print("1. Masculino")
                        print("2. Femenino")
                        g = int(input("Elige (1-2): ").strip())
                        if g == 1:
                            est["genero"] = "M"
                            print("✅ Género actualizado.")
                            break
                        elif g == 2:
                            est["genero"] = "F"
                            print("✅ Género actualizado.")
                            break
                        else:
                            print("⚠️ Opción inválida.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif op == 9:
                nuevo = input("Nuevo tipo de sangre: ").strip().upper()
                if nuevo:
                    est["sangre"] = nuevo
                    print("✅ Tipo de sangre actualizado.")
                else:
                    print("⚠️ Vacío, no se modificó.")
            elif op == 10:
                while True:
                    try:
                        print("Modalidad:")
                        print("1. Presencial")
                        print("2. Virtual")
                        print("3. Mixta")
                        m = int(input("Elige (1-3): ").strip())
                        if m == 1:
                            est["modalidad"] = "Presencial"
                            break
                        elif m == 2:
                            est["modalidad"] = "Virtual"
                            break
                        elif m == 3:
                            est["modalidad"] = "Mixta"
                            break
                        else:
                            print("⚠️ Opción inválida.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
                print("✅ Modalidad actualizada.")
            elif op == 11:
                while True:
                    try:
                        print("Situación académica:")
                        print("1. Regular")
                        print("2. Sabatino")
                        print("3. Dominical")
                        s = int(input("Elige (1-3): ").strip())
                        if s == 1:
                            est["situacion"] = "Regular"
                            break
                        elif s == 2:
                            est["situacion"] = "Sabatino"
                            break
                        elif s == 3:
                            est["situacion"] = "Dominical"
                            break
                        else:
                            print("⚠️ Opción inválida.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
                print("✅ Situación académica actualizada.")
            elif op == 12:
                nuevo = input("Nueva carrera: ").strip()
                if nuevo:
                    est["carrera"] = nuevo
                    print("✅ Carrera actualizada.")
                else:
                    print("⚠️ Vacío, no se modificó.")
            elif op == 13:
                while True:
                    try:
                        nuevo = int(input("Nuevo año (1,2,3,...): ").strip())
                        if nuevo > 0:
                            est["anio"] = nuevo
                            print("✅ Año actualizado.")
                            break
                        else:
                            print("⚠️ Debe ser positivo.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif op == 14:
                while True:
                    try:
                        nuevo = int(input("Nuevo ciclo (1 o 2): ").strip())
                        if nuevo in [1, 2]:
                            est["ciclo"] = nuevo
                            print("✅ Ciclo actualizado.")
                            break
                        else:
                            print("⚠️ Solo 1 o 2.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif op == 15:
                while True:
                    try:
                        nuevo = int(input("Nuevo semestre (1 o 2): ").strip())
                        if nuevo in [1, 2]:
                            est["semestre"] = nuevo
                            print("✅ Semestre actualizado.")
                            break
                        else:
                            print("⚠️ Solo 1 o 2.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
            elif op == 16:
                nuevo = input("Nueva área de conocimiento: ").strip()
                if nuevo:
                    est["area"] = nuevo
                    print("✅ Área actualizada.")
                else:
                    print("⚠️ Vacío, no se modificó.")
            elif op == 17:
                idiomas = []
                while True:
                    try:
                        cant = int(input("¿Cuántos idiomas domina ahora?: ").strip())
                        if cant >= 0:
                            break
                        else:
                            print("⚠️ Debe ser 0 o positivo.")
                    except ValueError:
                        print("⚠️ Ingresa un número válido.")
                for j in range(cant):
                    while True:
                        idi = input(f" - Idioma {j+1}: ").strip()
                        if idi:
                            idiomas.append(idi)
                            break
                        print("⚠️ No puede estar vacío.")
                est["idiomas"] = idiomas
                print("✅ Idiomas actualizados.")
            elif op == 18:
                nuevo = input("Nueva materia: ").strip()
                if nuevo:
                    est["materia"] = nuevo
                    print("✅ Materia actualizada.")
                else:
                    print("⚠️ Vacío, no se modificó.")
            elif op == 19:
                notas = []
                print("Ingrese las 4 notas (0-100):")
                for p in range(1, 5):
                    while True:
                        try:
                            n = float(input(f" Parcial {p}: ").strip())
                            if 0 <= n <= 100:
                                notas.append(n)
                                break
                            else:
                                print("⚠️ Debe estar entre 0 y 100.")
                        except ValueError:
                            print("⚠️ Ingresa un número válido.")
                est["notas"] = notas
                est["promedio"] = calcular_promedio(notas)
                print("✅ Notas y promedio actualizados.")
            elif op == 20:
                # actualizar fecha de modificación y salir
                est["ultima_modificacion"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("↩️ Volviendo...")
                break
            else:
                print("⚠️ Opción inválida.")

            # cada vez que se modifica algo actualizamos ultima_modificacion
            est["ultima_modificacion"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    except Exception as e:
        print(f"⚠️ Error al editar: {e}")

# -------------------------------
# Menú principal
# -------------------------------
def mostrar_menu():
    print("\n" + "="*50)
    print("🎓 MENÚ PRINCIPAL")
    print("="*50)
    print("1. Agregar estudiante")
    print("2. Buscar / Ver / Editar estudiante (por carnet)")
    print("3. Eliminar estudiante (por carnet)")
    print("4. Mostrar lista de estudiantes")
    print("5. Salir")

# -------------------------------
# Función principal
# -------------------------------
def main():
    print("="*50)
    print("✨ Bienvenido al Sistema de Control de Notas ✨")
    print("="*50)
    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción (1-5): ").strip()
            if opcion == "1":
                agregar_estudiante(estudiantes)
            elif opcion == "2":
                buscar_estudiante(estudiantes)
            elif opcion == "3":
                eliminar_estudiante(estudiantes)
            elif opcion == "4":
                mostrar_lista(estudiantes)
            elif opcion == "5":
                print("👋 Gracias por usar el sistema. ¡Hasta pronto!")
                break
            else:
                print("⚠️ Opción inválida. Intente de nuevo.")
        except Exception as e:
            print(f"⚠️ Error inesperado en el menú: {e}")

# Ejecutar programa
if __name__ == "__main__":
    main()

