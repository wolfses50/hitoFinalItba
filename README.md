# GUARDIANES DEL CLIMA
## Descripción:
Este es el repositorio del TP Final de la materia de tecnologia, el challenge de programacion "GuardianClimaITBA". 
## Uso:
Para ejecutar el programa, se debe correr el archivo `main.py` con Python 3.8 o superior. Asegurarse de tener instaladas las dependencias necesarias, que se pueden instalar con el siguiente comando:

```bash
pip install -r requirements.txt
```
## Estructura del proyecto:
contamos con un unico archivo `main.py` que contiene la logica del programa, y un archivo `requirements.txt` que contiene las dependencias necesarias para su ejecucion, dos archivos de csv `historial_gloabl.csv` y `usuarios_simulados.csv` que contienen los datos de los usuarios y el historial de todos los usuarios.
## Funcionamiento:
El archivo programa `main.py` contiene un buble princial que va mostrando opciones y una vez el usuario se autenntica, permite utilizar las distintas funciones del programa.
Es importante agregar un archivo `.env` con las variables de entorno necesarias para la ejecucion del programa con la siguiente estructura:

```
key=clave de la API de openweather
gemini=clave de la API de gemini
```

