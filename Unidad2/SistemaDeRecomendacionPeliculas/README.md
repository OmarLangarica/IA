
## Integrantes
* Carrillo Beltran Irvin Jair
* Langarica Ornelas Jesús Omar
# Tarea 2 Sistema de Recomendación de Peliculas

Este proyecto es una aplicación web que recomienda películas similares a partir de un título seleccionado por el usuario usando filtrado basado en contenido (TF-IDF).  El sistema combina un backend en Python con Flask y un frontend en React.



## Imagen
<img width="1674" height="1357" alt="Image" src="https://github.com/user-attachments/assets/58eef4d7-aa11-46b7-b373-8f266a618bdb" />

## Modelo utilizado
El sistema utiliza un modelo de recomendación basada en contenido, que compara características textuales de las películas como géneros, actores y directores para calcular su similitud.  
Las recomendaciones se generan mediante la similitud del coseno aplicada sobre representaciones TF-IDF de los datos textuales.
## Dependencias e instalacion 
**Backend**
* flask
* flask-cors
* pandas
* scikit-learn
* 
**Instalacion Backend**
* cd IA\Unidad2\SistemaDeRecomendacionPeliculas\backend
* python app.py

**Frontend**
* cd Unidad2\SistemaDeRecomendacionPeliculas\frontend
* npm install 
* npm start

## Funcionamiento
**Carga de Datos:**
El archivo movies.csv se lee con pandas y se combinan columnas relevantes (título, géneros, actores, director).

**Vectorización TF-IDF:**
Se convierte el texto en vectores numéricos representando la importancia de las palabras.

**Similitud del Coseno:**
Se calcula la similitud entre todas las películas.

**Recomendación:**
Dado un título, se ordenan las películas más similares y se devuelven las top_k.