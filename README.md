# Depura el código: Python y FastAPI
Este es el repositorio del curso de LinkedIn Learning `Depura el código: Python y FastAPI`. El curso completo está disponible en [LinkedIn Learning][lil-course-url].

![Nombre completo del curso][lil-thumbnail-url] 

Consulta el archivo Readme en la rama main para obtener instrucciones e información actualizadas.

Este curso está diseñado para desarrolladores que se especializan en el desarrollo backend con Python y FastAPI. Aprenderás a identificar y resolver eficazmente errores en API Rest construidas con FastAPI. El curso presenta una API desarrollada en FastAPI con errores, y te guiará a través del proceso de depuración para corregirlos. Si buscas perfeccionar tus habilidades en depuración de código y mejorar la calidad de tus proyectos de desarrollo backend, este curso será esencial para ti.

## Instrucciones
Este repositorio contiene una API Rest desarrollada con FastAPI, la API consiste en un sistema de creación de restaurantes y opiniones de restaurantes. Tiene dos ramas (branches): 

 * La rama `depura` contiene el código de la aplicación con los errores que se deben solucionar.
 * La rama `solucion` contiene el código de la aplicación sin errores.

## Instalación
1. Instala [Python](https://www.python.org/downloads/), se recomienda la última versión estable.
2. Para utilizar estos archivos de ejercicios puedes usar editores de código como Pycharm o VScode.
3. Clona este repositorio en tu máquina local usando la Terminal (macOS) o CMD (Windows), o una herramienta GUI como SourceTree.
4. Desde la terminal accede a alguna de las ramas `depura` o `solucion` y accede al directorio `api_calificacion`.
5. Crea un ambiente virtual de Python, puedes hacerlo con virtualenv usando los comandos

		pip install virtualenv
		virtualenv <reemplazar por nombre del ambiente>

7. Instala las librerías con el comando

		pip install -r requirements.txt

8.  Corre la aplicación con el comando

		uvicorn app.main:app --reload

9. Para correr las pruebas unitarias del código

   		coverage run -m pytest

### Docente

**Ana María Pinto**

Echa un vistazo a mis otros cursos en [LinkedIn Learning](https://www.linkedin.com/learning/instructors/ana-maria-pinto).

[0]: # (Replace these placeholder URLs with actual course URLs)
[lil-course-url]: https://www.linkedin.com/learning/building-a-graphql-project-with-react-js
[lil-thumbnail-url]: https://cdn.lynda.com/course/2875095/2875095-1615224395432-16x9.jpg


[1]: # (End of ES-Instruction ###############################################################################################)
