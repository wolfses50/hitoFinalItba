# GUARDIÁN DEL CLIMA
## Descripción:
Este es el repositorio del TP Final de la materia de tecnologia, el challenge de programacion "GuardianClimaITBA". 
## Uso:
Para ejecutar el programa, se debe correr el archivo `main.py` con Python 3.8 o superior. Asegurarse de tener instaladas las dependencias necesarias, que se pueden instalar con el siguiente comando:

```bash
pip install -r requirements.txt
```
## Estructura del proyecto:
Contamos con un unico archivo `main.py` que contiene la logica del programa, un archivo `requirements.txt` que contiene las dependencias necesarias para su ejecucion, dos archivos de csv `historial_gloabl.csv` y `usuarios_simulados.csv` que contienen los datos de los usuarios y el historial de todos los usuarios.

## Funcionamiento:
El archivo programa `main.py` contiene un bucle princial que va mostrando opciones. Una vez que se autentifican las credenciales del usuario, se tiene acceso a las distintas funciones del programa relacionadas con el clima.

Es importante agregar un archivo `.env` con las variables de entorno necesarias para la ejecucion del programa con la siguiente estructura:

```
key=clave de la API de openweather
gemini=clave de la API de gemini
```

