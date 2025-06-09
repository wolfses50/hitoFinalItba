import requests
import json 
import os
from dotenv import load_dotenv
load_dotenv()
running = True
autenticated = False
archivoUsuarios = "usuarios_simulados.csv"
historialGlobales = "historial_global.csv"
api_key = os.getenv("key")

def logIn():
        global autenticated
        userInput = input("Ingrese su nombre de usuario: ")
        passwordInput = input("Ingrese su contraseña: ")

        try:
            with open(archivoUsuarios, 'r') as archivo:
                for index, linea in enumerate(archivo):
                    user, password = linea.strip().split(',')
                    if user == userInput and password == passwordInput:
                        autenticated = True
                        print(f"Bienvenido, {userInput}!")
                        return
                print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
        except FileNotFoundError:
            print("Archivo de usuarios no encontrado. Por favor, registre un usuario primero.")
        
def register():
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")

    try:
        with open(archivoUsuarios, 'r') as archivo:
            for linea in archivo:
                user, _ = linea.strip().split(',')
                if user == username:
                    print("El nombre de usuario ya está registrado. Intente con otro.")
                    return
    except FileNotFoundError:
        pass
    #revisar que contra cumpla con 3 criterios vistos en clase
    with open(archivoUsuarios, 'a') as archivo:
        archivo.write(f"{username},{password}\n")
        print(f"Usuario {username} registrado exitosamente.")

def consultarClima():
    ciudad = input("Ingrese el nombre de la ciudad para consultar el clima: ").strip()
    if not ciudad:
        print("Error: Debes ingresar el nombre de una ciudad.")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': ciudad,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }

    print(f"\nConsultando el clima (OpenWeatherMap) para: {ciudad}...")
    try:
        response = requests.get(base_url, params=parametros, timeout=10)
        response.raise_for_status()
        datos_clima = response.json()

        # Verifica si se obtuvieron datos válidos
        if not datos_clima or 'main' not in datos_clima:
            print(f"No se pudieron obtener los datos del clima para '{ciudad}'.")
            return

        # Extraer datos del clima
        temperatura = datos_clima['main']['temp']
        sensacion_termica = datos_clima['main']['feels_like']
        humedad = datos_clima['main']['humidity']
        descripcion = datos_clima['weather'][0]['description']
        velocidad_viento = datos_clima['wind']['speed']

        # Mostrar los datos del clima
        print(f"\nClima en {ciudad.capitalize()}:")
        print(f"Temperatura: {temperatura}°C")
        print(f"Sensación Térmica: {sensacion_termica}°C")
        print(f"Humedad: {humedad}%")
        print(f"Descripción: {descripcion.capitalize()}")
        print(f"Velocidad del Viento: {velocidad_viento} m/s")

        # Guardar en historial global
        print("\nGuardando en historial global...")
        with open(historialGlobales, 'a') as archivo_historial:
            archivo_historial.write(f"{ciudad},{temperatura},{sensacion_termica},{humedad},{descripcion},{velocidad_viento}\n")

    except requests.exceptions.HTTPError as errh:
        if response.status_code == 401:
            print("Error de autenticación OWM: API Key inválida.")
        elif response.status_code == 404:
            print(f"Error OWM: Ciudad '{ciudad}' no encontrada.")
        else:
            print(f"Error HTTP OWM: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Error de conexión/petición OWM: {err}")
    except json.JSONDecodeError:
        print("Error OWM: La respuesta de la API no es JSON válido.")
    except KeyError:
        print("Error: Formato inesperado en los datos de OWM.")
    
def historialPersonal():
    try:
        with open(historialGlobales, 'r') as archivo_historial:
            historial = archivo_historial.readlines()
            ciudad = input("Ingrese el nombre de la ciudad para ver su historial: ").strip()
            if not ciudad:
                print("Error: Debes ingresar el nombre de una ciudad.")
                return
            print(f"\nHistorial de consultas para {ciudad.capitalize()}:")
            encontrado = False
            contador = 0 
            for linea in historial:
                # Verificar si la ciudad está en la línea (ignorando mayúsculas/minúsculas)
                if ciudad.lower() in linea.lower():
                    encontrado = True
                    contador += 1
                    datos = linea.strip().split(',')
                    print(f"nro:{contador}°\nCiudad: {datos[0]} \nTemperatura: {datos[1]}°C \nSensación Térmica: {datos[2]}°C \nHumedad: {datos[3]}% \nDescripción: {datos[4]} \nVelocidad del Viento: {datos[5]} m/s")
            if not encontrado:
                print(f"No se encontraron registros para la ciudad '{ciudad}' en el historial global.")
    except FileNotFoundError:
        print(f"Error: El archivo '{historialGlobales}' no existe. Asegúrate de que el historial global esté disponible.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def exportarHistorial():
    print("Función de exportación de historial no implementada aún.")

def ia():
    print("Función de IA no implementada aún.")
    
def acercaDe():
    print("Función de información acerca de no implementada aún.")

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
    