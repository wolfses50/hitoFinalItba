running = True
autenticated = False
while running:
    if autenticated == False:
        print("\n1. Iniciar Sesión:")
        print("2. Registrar Nuevo Usuario")
        print("3. Salir")

        option = input("\nElige una opción (1-3): ")
        match option:
            case "1":
                logIn()
            case "2":
                register()
            case "3":
                running = False
                print("Saliendo del programa. ¡Hasta luego!")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 3.")
    else:
        print("\n1. Consultar Clima Actual y Guardar en Historial Global")
        print("2. Ver Mi Historial Personal de Consultas por Ciudad") 
        print("3. Estadísticas Globales de Uso y Exportar Historial Completo")
        print("4. ¿Cómo Me Visto Hoy? 🧥🤖") 
        print("5. Acerca de...")
        print("6. Cerrar Sesión")

        option = input("\nElige una opción (1-6): ")
        match option:
            case "1":
                consultarClima()
            case "2":
                historialPersonal()
            case "3":
                exportarHistorial()            
            case "4":
                ia()
            case "5":
                acercaDe()
            case "6":
                autenticated = False
                print("Cerrando sesión. Por favor, inicia sesión nuevamente.")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 6.")
    def logIn():
        print("Función de inicio de sesión no implementada aún.")

    def register():
        print("Función de registro de usuario no implementada aún.")
    def consultarClima():
        print("Función de consulta de clima no implementada aún.")
    def historialPersonal():
        print("Función de historial personal no implementada aún.")
    def exportarHistorial():
        print("Función de exportación de historial no implementada aún.")
    def ia():
        print("Función de IA no implementada aún.")
    def acercaDe():
        print("Función de información acerca de no implementada aún.")