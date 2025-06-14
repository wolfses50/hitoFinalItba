# -- Importación de librerias, APIs, etc. --
from rich import print
import requests
import re
import random
import string
import google.generativeai as genai
import json
import os
# from env import api_gemini_key
from dotenv import load_dotenv
import datetime
load_dotenv()
running = True
autenticated = False
archivoUsuarios = "usuarios_simulados.csv"
historialGlobales = "historial_global.csv"
api_key = os.getenv("key")
gemini = os.getenv("gemini")
usernameg = ""

# -- Función para inicio de sesión --
def logIn():
    global autenticated
    while True:
        print("[bold blue]\n---------- INICIO DE SESIÓN ----------[/bold blue]")
        print("Si desea salir del inicio de sesión, escriba [underline]salir[/underline] ❌.")
        userInput = input("\n👤 Ingrese su nombre de usuario: ")
        if userInput.lower() == "salir":
            print("Volviendo al menú principal. 🔙")
            return
        else:
            confirmar = input(f"¿Confirma su nombre de usuario?: '{userInput}'\n\033[1mEscriba si/no: \033[0m")
            if confirmar.lower() != "si":
                print("[bold italic]Reiniciando inicio de sesión. 🔄[/bold italic]")
                continue #reinicia el bucle
            
        passwordInput = input("\n🔐 Ingrese su contraseña: ")
        if passwordInput.lower() == "salir":
            print("[bold italic]Reinician. 😢[/bold italic]")
            return
        else:
            confirmar = input("¿Confirmar contraseña e iniciar sesión?\n\033[1mEscriba si/no: \033[0m")
            if confirmar.lower() != "si":
                print("[bold italic]Reiniciando inicio de sesión. 🔄[/bold italic]")
                continue
        try:
            with open(archivoUsuarios, 'r') as archivo:
                for linea in archivo:
                    user, password = linea.strip().split(',')
                    if user == userInput and password == passwordInput:
                        autenticated = True
                        global usernameg
                        usernameg = userInput
                        print(f"[bold magenta]\nBienvenid@, {userInput}![/bold magenta]")
                        return
            print("[bold italic]Usuario o contraseña incorrectos. Inténtalo de nuevo. 🤔[/bold italic]")
        except FileNotFoundError:
            print(
                "[bold italic red]Archivo de usuarios no encontrado. Por favor, registre un usuario primero. 😥[/bold italic red]")
            return
        except Exception as e:
            print(f"[red]Error inesperado: {e}[/red]")
            return


# --- Función para validar contraseña segura ---
def validarContraseña(password):
    errores = []

    # Criterio 1: Longitud mínima de 15 caracteres
    if len(password) < 15:
        errores.append("[italic]tener al menos 15 caracteres[/italic]")

    # Criterio 2: Contener letras mayúsculas
    if not re.search(r"[A-Z]", password):
        errores.append("[italic]incluir al menos una letra mayúscula[/italic]")

    # Criterio 3: Contener letras minúsculas
    if not re.search(r"[a-z]", password):
        errores.append("[italic]incluir al menos una letra minúscula[/italic]")

    # Criterio 4: Contener al menos un número
    if not re.search(r"[0-9]", password):
        errores.append("[italic]incluir al menos un número[/italic]")

    # Criterio 5: Contener al menos un símbolo
    if not re.search(r"[!@#$%^&*()_\-+=]", password):
        errores.append("[italic]incluir al menos un símbolo (como !, @, #, etc.)[/italic]")
    return errores

# -- Función para generar una contraseña segura sugerida para el usuario --
def generarContraseñaSegura(longitud=16):
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()_-+="
    while True:
        password = ''.join(random.choice(caracteres) for _ in range(longitud))
        # Validamos con los mismos criterios que en validarContraseña()
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()_-+=" for c in password)):
            return password
        

# -- Función para registrar un nuevo usuario --
def register():
    while True:
        print("[bold blue]\n---------- REGISTRO DE USUARIO ----------[/bold blue]")
        # Pedimos el nombre de usuario y contraseña
        print("Si desea salir del registro de usuario, escriba [underline]salir[/underline]. ❌")
        username = input("👤 Ingrese un nombre de usuario: ")
        if username.lower() == "salir":
            print("[bold italic]Saliendo del registro de usuario. 😞[bold italic]")
            return
        else:
            confirmar = input(f"¿Confirmar nombre de usuario?: '{username}'\n\033[1mEscriba si/no: \033[0m")
            if confirmar.lower() != "si":
                print("[bold italic]Reiniciando registro de usuario. 🔄[bold italic]")
                continue
                
        try:
            # Verificamos que el usuario no este repetido
            with open(archivoUsuarios, 'r') as archivo:
                for linea in archivo:
                    # Recuperamos el usuario de cada línea
                    user, _ = linea.strip().split(',')
                    if user == username:
                        print("[bold italic red]El nombre de usuario ya está registrado. 🤔 Intente con otro.[/bold italic red]")
                        return
        except FileNotFoundError:
            print("Archivo no encontrado.💥⚠. Saliendo de inicio de sesión.")
            return
        except Exception as e:
            print(f"[red]Error inesperado: {e}[/red]. \nSaliendo de inicio de sesión.")
            return

        while True:
            password = input("🔐 Ingrese una contraseña: ")
            if password.lower() == "salir":
                print("[bold italic]Saliendo del registro.[bold italic]")
                return
            
            # Validamos que la contraseña cumpla los 5 criterios
            errores = validarContraseña(password)
            if len(errores) > 0:
                print("\n[red]Tu contraseña no es lo suficientemente segura.[/red]")
                print("No cumple con los siguientes criterios:")
                for error in errores:
                    print(f"[dim yellow]- Debe {error}[/dim yellow]")
                # Generamos y mostramos una sugerencia segura aleatoria
                sugerencia = generarContraseñaSegura()
                print("\nSugerencia: Usá una contraseña de al menos 15 caracteres, que incluya mayúsculas, minúsculas, números y símbolos. "
                "Te recomendamos que no se base en información personal, palabras comunes o patrones obvios, "
                "sino que sea lo mas aleatoria posible.")
                print(f"Ejemplo de contraseña segura: {sugerencia}")
                print("\nSi desea salir del registro de usuario, escriba [underline]salir[/underline]. ❌")
            else:    
                print("[green] Tu contraseña es segura. [/green]✅")
                passw = input(f"Reescriba contraseña: ")
                if passw == password:
                    pass
                else: 
                    print("[bold italic red]Las contraseñas no coinciden 🤨. Reinténtelo 🔄. [/bold italic red]")
                    continue  
                break

        # Guardamos el nuevo usuario y contraseña en el archivo
        with open(archivoUsuarios, 'a') as archivo:
            archivo.write(f"{username},{password}\n")
            print(f"[green]Usuario {username} registrado exitosamente. 😻[/green]")
            # Verificamos que el usuario esta auternticado para mandarlo al menu princial
            # Almacenamos el nombre de usuario en una variable publica
            global autenticated
            global usernameg
            usernameg = username
            autenticated = True
            return

# Función para consultar el clima de una ciudad usando la API de OpenWeatherMap
def consultarClima():
    # Pedimos el nombre de la ciudad
    print("Si desea volver al menú, escriba [underline]salir[/underline]. ❌")
    ciudad = input("Ingrese el nombre de la ciudad para consultar el clima: 🏙️\t  ").strip()
    if ciudad.lower() == "salir":
        print("[bold italic]Saliendo de la consulta del clima.[/bold italic]")
        return
    if not ciudad:
        print("[bold italic red]Error: Debes ingresar el nombre de una ciudad. 😡[/bold italic red]")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': ciudad,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }

    print(f"\nConsultando el clima (OpenWeatherMap) para: {ciudad} 🤔.")
    try:
        # Hacemos la request y recuperamos la respuesta en formato json
        response = requests.get(base_url, params=parametros, timeout=10)
        response.raise_for_status()
        datos_clima = response.json()

        # Verifica si se obtuvieron datos válidos
        if not datos_clima or 'main' not in datos_clima:
            print(f"[bold italic red]No se pudieron obtener los datos del clima para '{ciudad}'. ⚠[/bold italic red]"
                "Volviendo al menu principal 🔙")
            return

        # Extraer datos del clima
        temperatura = datos_clima['main']['temp']
        sensacion_termica = datos_clima['main']['feels_like']
        humedad = datos_clima['main']['humidity']
        descripcion = datos_clima['weather'][0]['description']
        velocidad_viento = datos_clima['wind']['speed']

        # Mostrar los datos del clima
        print(f"\n[bold]Clima en {ciudad.capitalize()} 🌤️...[/bold]")
        print(f"[bold]Temperatura:[/bold] [cyan]{temperatura}°C [/cyan]🌡️")
        print(f"[bold]Sensación Térmica:[/bold] [cyan]{sensacion_termica}°C [/cyan]🤒")
        print(f"[bold]Humedad:[/bold] [cyan]{humedad}% 💧")
        print(f"[bold]Descripción:[/bold] [cyan]{descripcion.capitalize()} 📖[/cyan]")
        print(f"[bold]Velocidad del Viento:[/bold] [cyan]{velocidad_viento} m/s 🍃[/cyan]")
        

        # Guardar en historial global
        print("\nGuardando en historial global.")
        # Levantamos la fecha y hora actual
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Almacenamos los datos en el archivo de historial global
        with open(historialGlobales, 'a') as archivo_historial:
            global usernameg
            usuario = usernameg if usernameg else "Anonimo"
            archivo_historial.write(
                f"{usuario},{ciudad},{fecha_hora},{temperatura},{sensacion_termica},{humedad},{descripcion},{velocidad_viento}\n")
        print("✅ Guardado")
        #return temperatura, ciudad, sensacion_termica, humedad, descripcion, velocidad_viento
        input("\033[1mPresione enter si quiere volver atrás.  \033[0m")
        print("[bold italic]Volviendo a menu principal 🔙[/bold italic]")
    
    # Manejo de errores de la API
    except requests.exceptions.HTTPError as errh:
        if response.status_code == 401:
            print("[red]Error de autenticación OWM: API Key inválida.[/red]"
            "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
            return
        elif response.status_code == 404:
            print(f"[red]Error OWM: Ciudad '{ciudad}' no encontrada.[/red]"
            "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
            return
        else:
            print(f"[red]Error HTTP OWM: {errh}[/red]"
            "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
            return
    except requests.exceptions.RequestException as err:
        print(f"[red]Error de conexión/petición OWM: {err}[/red]"
        "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
        return
    except json.JSONDecodeError:
        print("[red]Error OWM: La respuesta de la API no es JSON válido.[/red]"
        "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
        return
    except KeyError:
        print("[red]Error: Formato inesperado en los datos de OWM.[/red]"
        "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
        return
    
# Función para ver el historial personal de consultas por ciudad
def historialPersonal():
    try:
        with open(historialGlobales, 'r') as archivo_historial:
            print("Si desea volver al menu, escriba [underline]salir[/underline]. ❌")
            # Abrimos el historial global y pedimos por la ciudad
            historial = archivo_historial.readlines()
            ciudad = input("Ingrese el nombre de la ciudad para ver su historial: 🏙️ \t ").strip()
            if ciudad.lower() == "salir":
                print("Saliendo del historial personal. 🔙")
                return
            if not ciudad:
                print("[red]Error: Debes ingresar el nombre de una ciudad.[/red]")
                return
            print(f"\nTu historial de consultas para {ciudad.capitalize()}:")
            encontrado = False
            contador = 0
            # Establecemos un contador para mostrar el nro de consultas
            # Y un booleano para saber si ya se encontró la ciudad, sino
            # mostramos un mensaje de error diciendo que no se encontró en ninguna de sus consultas registradas
            for linea in historial:
                # Verificar si la ciudad está en la línea (ignorando mayúsculas/minúsculas)
                # y si el usuario autenticado es el que hizo la consulta
                if ciudad.lower() in linea.lower() and usernameg.lower() in linea.lower():
                    encontrado = True
                    # Si se encuentra, incrementamos el contador y mostramos los datos
                    contador += 1
                    datos = linea.strip().split(',')
                    print(
                        f"[bold white]nro:{contador}°[bold white]"
                        f"\n[bold]Ciudad 🏙️:[bold] [cyan]{datos[1]}[/cyan]"
                        f"\n[bold]Temperatura 🌡️:[bold] [cyan]{datos[3]}°C [/cyan]"
                        f"\n[bold]Sensación Térmica 🤒:[bold] [cyan]{datos[4]}°C [/cyan]"
                        f"\n[bold]Humedad 💧:[bold] [cyan]{datos[5]}% [/cyan]"
                        f"\n[bold]Descripción 📖:[bold] [cyan]{datos[6]} [/cyan]"
                        f"\n[bold]Velocidad del Viento 🍃:[bold] [cyan]{datos[7]} m/s [/cyan]"
                        f"\n[bold]Fecha y Hora ⏱️:[bold] [cyan]{datos[2]}\n[/cyan]")
            if not encontrado:
                print(
                    f"[yellow]No se encontraron registros para la ciudad '{ciudad}' en el historial personal. 🤯[/yellow]")
            input("\033[1mPresione enter si quiere volver atrás. \033[0m") #una vez que tereminó de ver todos los registros personales pregunta por volver
            print("[bold italic]Volviendo a menu principal 🔙[/bold italic]")
            return
    # Manejo de errores al abrir el archivo
    except FileNotFoundError:
        print(
            f"[red]Error: El archivo '{historialGlobales}' no existe. Asegúrate de que el historial global esté disponible.[/red]"
        "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
        return
    except Exception as e:
        print(f"[red]Error inesperado: {e}[/red]"
        "\n Volviendo a menu principal.") # OWM: OpenWeatherMap
        return

# Función para exportar el historial global y mostrar estadísticas de uso globales
def exportarHistorialEstadisticas():
    try:
        with open(historialGlobales, 'r') as archivo_historial:
            historial = archivo_historial.readlines()
            if not historial:
                print("[yellow]El historial global está vacío. No hay datos para analizar.[/yellow]"
                      "\nVolviendo al menu principal.")
                return

            # Saltar el encabezado
            if historial[0].strip().startswith("usuario"):
                historial = historial[1:]

            # Contar las apariciones de cada ciudad
            # y alcamcenamos todas las temperaturas para luego sacar la promedio
            conteo_ciudades = {}
            temperaturas = []
            for linea in historial:
                datos = linea.strip().split(',')
                #Usamos coma como separador de campos y ponemos en minisculas
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
            max_consultas = max(conteo_ciudades.values())
            ciudades_mas_consultadas = [ciudad for ciudad, cantidad in conteo_ciudades.items() if cantidad == max_consultas]

            # Calcular el número total de consultas
            total_consultas = len(historial)
            temp_promedio = sum(temperaturas) / len(temperaturas)

            #Mostramos las estadísticas
            print(f"\n========== ESTADÍSTICAS GLOBALES DEL HISTORIAL 🌎 ==========")
            print(f"- Número total de consultas realizadas: {total_consultas}")
            if len(ciudades_mas_consultadas) == 1:
                print(f"- La ciudad con más consultas es '{ciudades_mas_consultadas[0].capitalize()}' 👑 con {max_consultas} consultas.")
            else:
                ciudades_str = ', '.join([c.capitalize() for c in ciudades_mas_consultadas])
                print(f"- Las ciudades con más consultas son: {ciudades_str} 👑, cada una con {max_consultas} consultas.")
                print(f"- Temperatura promedio entre todas las consultas: [cyan]{temp_promedio:.2f}°C 🌡️[cyan]")
            input("\033[1mPresione enter si quiere volver atrás. \033[0m")
            print("[bold italic]Volviendo a menu principal 🔙[/bold italic]") #una vez que ya se analizó todo, preugnta por vovler
            return
    #Manejo de errores al abrir el archivo
    except FileNotFoundError:
        print(
            f"[red]Error: El archivo '{historialGlobales}' no existe. Asegúrate de que el historial global esté disponible.[/red]"
            "\nVolviendo al menu principal.")
        return
    except Exception as e:
        print(f"[red]Error inesperado: {e}[/red]"
        "\nVolviendo al menu principal.")
        return
    
# Función de IA
def ia(temperatura, sensacion_termica, viento, humedad, condicion_climatica, ciudad):
     
     #obtiene un consejo  de vestimenta de gemini
    try: 
        genai.configure(api_key=gemini)
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt_diseñado_por_equipo = (
    f"""Estás embebido en un programa de consola desarrollado por estudiantes del ITBA.
    Se te proporcionan datos del clima actual y tu tarea es generar un CONSEJO DE VESTIMENTA.

    IMPORTANTE:
    - NO debes incluir funciones de Python como print(), ni declarar variables, ni envolver la respuesta en código.
    - Tu salida debe ser un **string plano formateado** como si fuera la respuesta directa a mostrar en consola.
    - Disponemos de la librería [rich](https://rich.readthedocs.io/) para formateo en consola. Puedes usar etiquetas como:
    [bold], [italic], [cyan], [yellow], [green], [blue], etc. para resaltar partes del texto.
    - Incluí EMOJIS relevantes al clima y a la vestimenta (🌧️🧥☀️👕☂️🧢🧣🕶️) para hacerlo más atractivo.
    - Sé claro, conciso y práctico. El consejo debe mencionar:
    - Qué tipo de ropa usar
    - Si es necesario llevar paraguas, abrigo, protector solar, etc.

    Datos del clima:
    Ciudad: {ciudad}
    Temperatura: {temperatura}°C
    Sensación Térmica: {sensacion_termica}°C
    Humedad: {humedad}%
    Condición Climática: {condicion_climatica}
    Velocidad del Viento: {viento} m/s

    Tu respuesta debe ser SOLO el texto final que se mostrará al usuario en consola, utilizando rich y emojis según corresponda. No olvides dejar lineas entre el texto para que sea más legible.
    segui el siguiente formato de ejemplo:
    '¡Atención, Buenos Aires! 🌧️ Con 10.33°C y llovizna, te recomiendo:

    🧥 Abrigo impermeable o rompevientos.
    🧣 Bufanda y guantes para mayor confort.
    ☂️ No olvides el paraguas o piloto.
    👕 Opta por capas de ropa para adaptarte a los cambios de temperatura.
    ¡Que tengas un buen día!'

    """
    )
        print("\n ⚙️⚙️⚙️    Generando consejo de vestimenta con IA    ⚙️⚙️⚙️")
        response = model.generate_content(prompt_diseñado_por_equipo)
        if response.text:
            print(response.text)
            return response.text
        else:
            print("La IA no pudo generar un consejo. Razón (si está disponible):", response.prompt_feedback)
            return "No se pudo generar un consejo en este momento."
                #genera el contenido
    except Exception as e:
        print(f"[red]Error al contactar la API de Gemini o procesar la respuesta: {e}[/red]")
        return "[red]Error al generar el consejo de IA.[/red]"
#funcion para extraer la info del historial_global.csv para usar en la ia
def obtenerUltimoRegistroUsuario():
     try:
         with open(historialGlobales, 'r') as archivo:
             lineas = archivo.readlines()
             # Buscar desde el final el último registro del usuario autenticado
             for linea in reversed(lineas):
                 datos = linea.strip().split(',')
                 if datos[0] == usernameg:
                     return {
                         "usuario": datos[0],
                         "ciudad": datos[1],
                         "fecha": datos[2],
                         "temperatura": float(datos[3]),
                         "sensacion_termica": float(datos[4]),
                         "humedad": int(datos[5]),
                         "descripcion": datos[6],
                         "velocidad_viento": float(datos[7])
                     }
         print("No se encontraron registros en el historial para el usuario.")
         return None
     except FileNotFoundError:
         print(f"[red]Error: El archivo '{historialGlobales}' no existe.[/red]")
         return None
     except Exception as e:
         print(f"[red]Error inesperado al leer el historial: {e}[/red]")
         return None


# función para mostrar información acerca del programa
def acercaDe():
        print("""
    ===== [bold magenta]Acerca de...[/bold magenta] =====
    Guardían Clima ITBA es una aplicación interactiva con fines
    educativos. Permite a los usuarios consultar datos sobre el
    clima actual de distintas ciudades, guardar y acceder a un
    historial personal y uno global, y a pedir a una IA
    recomendaciones de vestimenta acorde al clima.    
            
    -------------[magenta] 🧩 Uso 🧩[/magenta]-------------
    En el menu de inicio, el usuario puede elegir [bold]iniciar sesión[/bold],
    [bold]salir del programa[/bold] o [bold]registrarse[/bold]. En cuanto al último, se 
    implementaron criterios estrictos para usar contraseñas robustas.
    Una vez iniciada la sesión, el usuario puede acceder a
    diferentes opciones:
     🔹 [bold]Consular el clima actual de una ciudad a elección[/bold], mediante
        la API de OpenWeatherMap. Los datos de esta consulta son
        guardados junto con el nombre de usuario y la fecha y hora.
     🔹 [bold]Historial personal de consultas[/bold] anteriores del usuario, 
        filtradas por ciudad especificada.
     🔹 [bold]Estadísticas globales[/bold]: analiza el historial de consultas completo
        para calcular la ciudad más consultada, temperatura promedio y el
        total de búsquedas. Además, genera un archivo CSV listo para ser 
        graficado.
     🔹 [bold]Asistente de vestimenta con IA[/bold] según el clima recién consultado, 
        usando Google Gemini.
    -------------------------------------
            
    -------[magenta] ⚠ Precauciones ⚠ [/magenta]-------
    El programa almacena las credenciales como son cargadas
    y no implementa medidas de seguridad avanzadas. Esto se debe a
    que el programa es solo para uso educativo y no debe usarse con
    claves reales.
    Existe el "hasheo" el cual permite trasncirbir las contraeñas
    a un formato no legible e irreversible. Pero se puede comparar
    con la contraseña ingresada por el usuario, para saber si es
    correcta o no.
    Tanto la IA como la API para datos de clima son ajenas a nostros.
    No contamos con control sobre ellas y el uso de los datos que se
    inregesan en esta.
    ---------------------------------
            
    -----[magenta] 👥 Equipo desarrollador 👥 [/magenta]-----
    "Los Pros"
    1. Ulises Wolfzun
    2. Julieta Guerson
    3. Ana Gerli
    4. Dalila Ayelen Sardi
    5. Sofia Patron Costas
    --------------------------------
    """)


while running:
    # Mostramos el menú de iniicio siempre y cuando el usuario no este autenticado
    # Y el bool running sea False, es decir que no se "salio" del programa
    if autenticated == False:
        print ("\n[bold blue]=========== Bienvenido a Guardián Clima ===========[/bold blue]")
        print("\n1. Iniciar Sesión: 🪪")
        print("2. Registrar Nuevo Usuario: 📝")
        print("3. Salir del Programa: ❌")

        option = input("\n\033[1mElige una opción (1-3): \033[0m")
        match option:
            case "1":
                logIn()
            case "2":
                register()
            case "3":
                # Si el usuario elige salir, cambiamos el bool running a False
                running = False
                print("[bold italic]Saliendo del programa. ¡Hasta luego! 👋[/bold italic]")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 3. 😡")
    else:
        # Osea el usuario SI esta autenticado aqui

        print("\n============== MENU PRINCIPAL ===============")
        print("\n1. Consultar Clima Actual y Guardar en Historial Global 🌤️")
        print("2. Ver Mi Historial Personal de Consultas por Ciudad 🙍")
        print("3. Estadísticas Globales de Uso y Exportar Historial Completo 📊")
        print("4. ¿Cómo Me Visto Hoy? 🧥🤖")
        print("5. Acerca de... ❓")
        print("6. Cerrar Sesión 🔒")

        option = input("\n\033[1mElige una opción (1-6): \033[0m")
        match option:
            case "1":
                consultarClima()
            case "2":
                historialPersonal()
            case "3":
                exportarHistorialEstadisticas()
            case "4":
                #PRIMERO EXTRAIGO LA INFO DEL ULTIMO REGISTRO
                datos = obtenerUltimoRegistroUsuario()
                #si existen estos datos --> se asignan a cada parametro
                if datos:
                    ia(
                        temperatura=datos["temperatura"],
                        sensacion_termica=datos["sensacion_termica"],
                        viento=datos["velocidad_viento"],
                        humedad=datos["humedad"],
                        condicion_climatica=datos["descripcion"],
                        ciudad=datos["ciudad"]
                    )
                else:
                    print("Error al obtener el último registro del usuario.")
                input("\033[1mPresione enter si quiere volver atrás. \033[0m")
                print("[bold italic]Volviendo a menu principal 🔙[/bold italic]")
                continue
            case "5":
                acercaDe()
                input("\033[1mPresione enter si quiere volver atrás. \033[0m")
                print("[bold italic]Volviendo a menu principal 🔙[/bold italic]")
                continue
            case "6":
                # Si el usuario elige cerrar sesión, cambiamos el bool autenticated a False
                # y vuelve al bucle del menú de inicio
                autenticated = False
                print(f"Cerrando sesión. 👋➡")
            case _:
                print("Opción no válida, por favor elige una opción del 1 al 6. 😡")
