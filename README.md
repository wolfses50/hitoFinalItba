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
Crear un archivo llamado .env en la raíz del proyecto con el siguiente contenido:

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
El archivo programa `main.py` contiene un bucle princial que va mostrando opciones. Una vez que se autentifican las credenciales del usuario, se tiene acceso a las distintas funciones del programa relacionadas con el clima.

Al registrarse un usuario por primera vez, se le pedirá que su contraseña cumpla con ciertos criterios mínimos de seguridad, entre ellos que contenga al menos 12 caracteres, que incluya mayúsculas, minúsculas, números y símbolos.
