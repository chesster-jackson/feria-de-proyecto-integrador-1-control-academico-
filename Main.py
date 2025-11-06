from Body import cargar_datos , animacion , mostrar_historial , mostrar_lista , mostrar_pendientes , agregar_estudiante , SalirOperacion , buscar_estudiante , eliminar_estudiante , generar_pdf
#Aqui solo va el main y menu
#Menu de opciones 
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

#El main
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
                print(" Regresando al menú principal...")
                continue
            mostrar_pendientes()

        else:
            print(" Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
