# GUARDIÁN DEL CLIMA

## Descripción:
Este es el repositorio del TP Final de la materia de tecnologia, el challenge de programacion "GuardianClimaITBA". Es una aplicación de consola interactiva que permite a los usuarios consultar el clima de cualquier ciudad, guardar su historial, recibir recomendaciones de vestimenta con IA y generar estadísticas globales.

## Uso:
Para ejecutar el programa,
    1. Asegurate de tener Python 3.8 o superior instalado.
    2. Instalar las dependencias necesarias con:

    ```bash
    pip install -r requirements.txt
    ```

    3. Crear un archivo .env con tus claves de API (ver más abajo).
    4. Ejecutar el archivo principal:

    ```bash
    python main.py
    ```

## Requisistos del sistema:
1. Python 3.8 o superior
2. Conexión a Internet
3. Sistema operativo: Windows, macOS o Linux

## Variables de Entorno (.env)
Crear un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```ini
key=TU_API_KEY_DE_OPENWEATHERMAP
gemini=TU_API_KEY_DE_GEMINI
```
Estas claves se usan para acceder a:
    OpenWeatherMap (consultar clima actual)
    Google Gemini (sugerencias de vestimenta mediante IA)

## Estructura del proyecto:
Contamos con un unico archivo `main.py` que contiene la logica del programa, un archivo `requirements.txt` que contiene las dependencias necesarias para su ejecucion, dos archivos de csv `historial_gloabl.csv` y `usuarios_simulados.csv` que contienen los datos de los usuarios y el historial de todos los usuarios.

```bash
├── main.py
├── requirements.txt
├── historial_global.csv
├── usuarios_simulados.csv
├── .env
└── README.md
```

## Funcionamiento:
El archivo programa `main.py` contiene un bucle princial que va mostrando opciones. Una vez que se autentifican las credenciales del usuario, se tiene acceso a las distintas funciones del programa relacionadas con el clima:

    1. Consultar el clima actual de una ciudad (con datos como temperatura, humedad, viento, etc.).
    2. Guardar automáticamente cada consulta en un historial global.
    3. Ver su historial personal filtrado por ciudad.
    4. Ver estadísticas de uso a nivel global (ciudad más consultada, temperatura promedio, etc.).
    5. Recibir un consejo de vestimenta personalizado generado con IA (Google Gemini).
    6. Ver información del programa y sus autores.
    7. Cerrar sesión para volver al menú de acceso.

## Validación de Contraseñas
Al registrarse un usuario por primera vez, el sistema valida que su contraseña cumpla con al menos 3 de los siguientes 5 criterios mínimos de seguridad:

    1. Longitud mínima de 12 caracteres
    2. Incluir al menos una letra mayúscula
    3. Incluir al menos una letra minúscula
    4. Incluir al menos un número
    5. Incluir al menos un símbolo (como !@#$%^&*)

Si la contraseña no cumple, el programa muestra claramente qué criterios no fueron cumplidos y sugiere una contraseña segura generada aleatoriamente.

Ejemplo sugerido por el sistema:
```bash
Ejemplo de contraseña segura: T3k@WzrNp1$aqPZc
```

## Manejo de Archivos
usuarios_simulados.csv: Contiene nombre de usuario y contraseña. Las contraseñas están en texto plano por fines educativos.

historial_global.csv: Guarda todas las consultas climáticas con:
    Usuario
    Ciudad
    Fecha y hora
    Temperatura
    Sensación térmica
    Humedad
    Descripción del clima
    Velocidad del viento

## Estadísticas Globales
La aplicación analiza todos los registros del archivo historial_global.csv y calcula:

    Ciudad más consultada (o ciudades empatadas)
    Número total de consultas
    Temperatura promedio global
    Este archivo puede usarse luego para generar gráficos de barra, línea o torta (fuera del programa, con Excel o Google Sheets).

## Inteligencia Artificial
Se utiliza la API de Google Gemini para generar un consejo de vestimenta personalizado, según:
    Ciudad
    Temperatura
    Sensación térmica
    Condición climática
    Humedad
    Viento

La respuesta de la IA es decorada con emojis y redactada amigablemente para ser leída en consola.

## Precauciones
Este programa es educativo y no implementa cifrado real de contraseñas.
No se recomienda usar contraseñas reales en este sistema.
El acceso a las APIs depende de proveedores externos (OpenWeatherMap y Google Gemini).
La respuesta de la IA puede variar y no siempre será precisa.

## Créditos
Grupo: 

    Ulises Wolfzun

    Julieta Guerson

    Ana Gerli

    Dalila Ayelen Sardi

    Sofía Patrón Costas

Proyecto desarrollado para el Challenge Tecnológico Integrador - ITBA.