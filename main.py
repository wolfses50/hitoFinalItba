import requests
from google import genai
import json
import os
from dotenv import load_dotenv
import datetime
load_dotenv()
running = True
autenticated = False
archivoUsuarios = "usuarios_simulados.csv"
historialGlobales = "historial_global.csv"
api_key = os.getenv("key")
usernameg = ""

# Funcion para inicio de sesion


def logIn():
    global autenticated
    while True:
        print("Si desea salir del inicio de sesión, escriba 'salir'.")
        userInput = input("Ingrese su nombre de usuario: ")
        if userInput.lower() == "salir":
            print("Saliendo del inicio de sesión.")
            return
        passwordInput = input("Ingrese su contraseña: ")
        if passwordInput.lower() == "salir":
            print("Saliendo del inicio de sesión.")
            return
        try:
            with open(archivoUsuarios, 'r') as archivo:
                for linea in archivo:
                    user, password = linea.strip().split(',')
                    if user == userInput and password == passwordInput:
                        autenticated = True
                        global usernameg
                        usernameg = userInput
                        print(f"Bienvenido, {userInput}!")
                        return
            print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
        except FileNotFoundError:
            print(
                "Archivo de usuarios no encontrado. Por favor, registre un usuario primero.")
            return

# Función para registrar un nuevo usuario


def register():
    # pedimos el nombre de usuario y contraseña
    print("Si desea salir del inicio de sesión, escriba 'salir'.")
    username = input("Ingrese un nombre de usuario: ")
    if username.lower() == "salir":
        print("Saliendo del registro.")
        return
    password = input("Ingrese una contraseña: ")
    if password.lower() == "salir":
        print("Saliendo del registro.")
        return
    try:
        # Verificamos que el usuario no este repetido
        with open(archivoUsuarios, 'r') as archivo:
            for linea in archivo:
                # Recuperamos el usuario de cada línea
                user, _ = linea.strip().split(',')
                if user == username:
                    print("El nombre de usuario ya está registrado. Intente con otro.")
                    return
    except FileNotFoundError:
        pass
    # revisar que contra cumpla con 3 criterios vistos en clase --> SOFI

    # Guardamos el nuevo usuario y contraseña en el archivo
    with open(archivoUsuarios, 'a') as archivo:
        archivo.write(f"{username},{password}\n")
        print(f"Usuario {username} registrado exitosamente.")
        # Verificamos que el usuario esta auternticado para mandarlo al menu princial
        # Almacenamos el nombre de usuario en una variable publica
        global autenticated
        global usernameg
        usernameg = username
        autenticated = True

# Función para consultar el clima de una ciudad usando la API de OpenWeatherMap


def consultarClima():
    # Pedimos el nombre de la ciudad
    print("Si desea salir del inicio de sesión, escriba 'salir'.")
    ciudad = input(
        "Ingrese el nombre de la ciudad para consultar el clima: ").strip()
    if ciudad.lower() == "salir":
        print("Saliendo de la consulta del clima.")
        return
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
        # Hacemos la request y recuperamos la respuesta en formato json
        response = requests.get(base_url, params=parametros, timeout=10)
        response.raise_for_status()
        datos_clima = response.json()

        # Verifica si se obtuvieron datos válidos
        if not datos_clima or 'main' not in datos_clima:
            print(
                f"No se pudieron obtener los datos del clima para '{ciudad}'.")
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
        # Levantamos la fecha y hora actual
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Almacenamos los datos en el archivo de historial global
        with open(historialGlobales, 'a') as archivo_historial:
            global usernameg
            usuario = usernameg if usernameg else "Anonimo"
            archivo_historial.write(
                f"{usuario},{ciudad},{fecha_hora},{temperatura},{sensacion_termica},{humedad},{descripcion},{velocidad_viento}\n")
    # Manejo de errores de la API
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

# Función para ver el historial personal de consultas por ciudad


def historialPersonal():
    try:
        with open(historialGlobales, 'r') as archivo_historial:
            historial = archivo_historial.readlines()
            # Abrimos el historial global y pedimos por la ciudad
            ciudad = input(
                "Ingrese el nombre de la ciudad para ver su historial: ").strip()
            print("Si desea salir del inicio de sesión, escriba 'salir'.")
            if ciudad.lower() == "salir":
                print("Saliendo del historial personal.")
                return
            if not ciudad:
                print("Error: Debes ingresar el nombre de una ciudad.")
                return
            print(f"\nHistorial de consultas para {ciudad.capitalize()}:")
            encontrado = False
            contador = 0
            # Establecemos un contador para mostrar el nro de consultas
            # Y un booleano para saber si ya se encontró la ciudad, sino
            # mostramos un mensaje de error diciendo que no se encontraron
            # registros sobre aquella
            for linea in historial:
                # Verificar si la ciudad está en la línea (ignorando mayúsculas/minúsculas)
                # y si el usuario autenticado es el que hizo la consulta
                if ciudad.lower() in linea.lower() and usernameg.lower() in linea.lower():
                    encontrado = True
                    # Si se encuentra, incrementamos el contador y mostramos los datos
                    contador += 1
                    datos = linea.strip().split(',')
                    print(
                        f"nro:{contador}°\nCiudad: {datos[1]} \nTemperatura: {datos[2]}°C \nSensación Térmica: {datos[3]}°C \nHumedad: {datos[4]}% \nDescripción: {datos[5]} \nVelocidad del Viento: {datos[6]} m/s \nFecha y Hora: {datos[7]}\n")
            if not encontrado:
                print(
                    f"No se encontraron registros para la ciudad '{ciudad}' en el historial personal.")
    # Manejo de errores al abrir el archivo
    except FileNotFoundError:
        print(
            f"Error: El archivo '{historialGlobales}' no existe. Asegúrate de que el historial global esté disponible.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función para exportar el historial global y mostrar estadísticas de uso globales


def exportarHistorialEstadisticas():
    try:
        with open(historialGlobales, 'r') as archivo_historial:
            # Verificamos si el archivo de historial global no esté vacío
            historial = archivo_historial.readlines()
            if not historial:
                print("El historial global está vacío. No hay datos para analizar.")
                return

            # Contar las apariciones de cada ciudad
            # y alcamcenamos todas las temperaturas para luego sacar la promedio
            conteo_ciudades = {}
            temperaturas = []
            for linea in historial:
                datos = linea.strip().split(',')
                # Convertir a minúsculas para evitar problemas de mayúsculas/minúsculas
                ciudad = datos[1].lower()
                temperatura = float(datos[3])
                temperaturas.append(temperatura)
                # Agregamos la temrpatura a la lista
                # Contamos las apariciones de cada ciudad
                if ciudad in conteo_ciudades:
                    conteo_ciudades[ciudad] += 1
                else:
                    conteo_ciudades[ciudad] = 1

            # Usamos max() para encontrar la ciudad con el mayor número de consultas.
            # Después, guardamos cuántas veces fue consultada esa ciudad.
            ciudad_mas_consultada = max(
                conteo_ciudades, key=conteo_ciudades.get)
            cantidad_consultas = conteo_ciudades[ciudad_mas_consultada]

            # Calcular el número total de consultas
            total_consultas = len(historial)
            temp_promedio = sum(temperaturas) / len(temperaturas)
            # Mostrar estadísticas
            print(f"\nEstadísticas globales del historial:")
            print(f"- Número total de consultas realizadas: {total_consultas}")
            print(
                f"- La ciudad con más consultas es '{ciudad_mas_consultada.capitalize()}' con {cantidad_consultas} consultas.")
            print(
                f"- Temperatura promedio entre todas las consultas: {temp_promedio:.2f}°C")
    # Manejo de errores al abrir el archivo
    except FileNotFoundError:
        print(
            f"Error: El archivo '{historialGlobales}' no existe. Asegúrate de que el historial global esté disponible.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Función de IA (placeholder, aún no implementada)

def ia(api_key_gemini, temperatura, condicion_climatica, viento, humedad):
    client = genai.Client(api_key=api_key_gemini)
     
     #obtiene un consejo  de vestimenta de gemini
    print("Función de IA no implementada aún.")
    try: 
        genai.configure(api_key=api_key_gemini)
        model = genai.GenerativeModel('gemini-pro')
        prompt_diseñado_por_equipo = (
         f"Que me pongo hoy ?"   
        )
        print("\nGenerando consejo de vestimenta con IA...")
        response = model.generate_content(prompt_diseñado_por_equipo)
        if response.text:
            return response.text
        else:
            print("La IA no pudo generar un consejo. Razón (si está disponible):", response.prompt_feedback)
            return "No se pudo generar un consejo en este momento."
                #genera el contenido
    except Exception as e:
        print(f"Error al contactar la API de Gemini o procesar la respuesta: {e}")
        return "Error al generar el consejo de IA."
# función para mostrar información acerca del programa


def acercaDe():
        print("""
===Acerca de===
Este programa se llama GuardianClimaITBA
y es una aplicación de consola que permite 
a los usuarios consultar el clima actual de
diferentes ciudades, registrar sus consultas 
y ver estadísticas globales de uso. 
===============
          
===Uso===
Los usuarios pueden iniciar sesión, registrarse,
consultar el clima, ver su historial personal,
exportar estadísticas globales y recibir recomendaciones
de vestimenta basadas en el clima actual.
==========
          
===Precauciones===
El programa almacena las credenciales como son cargadas
y no implementa medidas de seguridad avanzadas. Es solo
para uso educativo y no debe usarse con claves reales.
Existe el "hasheo" el cual permite trasncirbir las contraeñas
a un formato no legible e irreversible. Pero se puede comparar
con la contraseña ingresada por el usuario. Y asi saber si es
correcta o no.
Tanto la IA como la API para datos de clima son ajenas a nostros
no contamos con control sobre ellas. Y el uso de los datos que se
inrgesan en esta
==================

falta: 
▪ Obtención de datos de clima y guardado de historial global.
▪ Generación de estadísticas globales y preparación del CSV
para gráficos.
          
===Miembros===
"Los Pros"
1. Ulises Wolfzun
2. Julieta Guerson
3. Ana Gerly
4. Dalila Sardi
5. Sofia Patron
==============
""")


while running:
    # Mostramos el menú de iniicio siempre y cuando el usuario no este autenticado
    # Y el bool running sea False, es decir que no se "salio" del programa
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
                # Si el usuario elige salir, cambiamos el bool running a False
                running = False
                print("Saliendo del programa. ¡Hasta luego!")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 3.")
    else:
        # Osea el usuario SI esta autenticado aqui
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
                exportarHistorialEstadisticas()
            case "4":
                ia()
            case "5":
                acercaDe()
            case "6":
                # Si el usuario elige cerrar sesión, cambiamos el bool autenticated a False
                # y vuelve al bucle del menú de inicio
                autenticated = False
                print("Cerrando sesión. Por favor, inicia sesión nuevamente.")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 6.")
