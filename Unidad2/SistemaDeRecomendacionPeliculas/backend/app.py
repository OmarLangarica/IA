from flask import Flask, jsonify, request      # Flask para crear el servidor web y manejar peticiones
from recomendador import Recomendador          # Importamos el recomendador
from flask_cors import CORS                    # Para permitir peticiones desde otros orígenes
import os                                      # Para manejar rutas de archivos del sistema operativo

app = Flask(__name__)
CORS(app)

# Obtenemos la ruta absoluta del directorio actual en donde se encuentra el archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construimos la ruta completa hacia el archivo CSV con los datos de películas
CSV_PATH = os.path.join(BASE_DIR, 'movies.csv')

# Creamos una instancia del recomendador con el archivo de datos
reco = Recomendador(CSV_PATH)

# Endpoint para obtener la lista completa de películas disponibles
@app.route('/movies', methods=['GET'])
def peliculas():
    # Llamamos al método del recomendador que devuelve las películas como una lista de diccionarios
    peliculas = reco.listar_peliculas()

    # Retornamos la lista en formato JSON 
    return jsonify({'movies': peliculas})

# Endpoint para obtener recomendaciones basadas en el título de una película
@app.route('/recommendations', methods=['GET'])
def recomendaciones():
    # Obtenemos el parámetro 'title' de la URL 
    titulo = request.args.get('title')

    # Si el cliente no envió un título, devolvemos un error 400 (Bad Request)
    if not titulo:
        return jsonify({'error': 'title parameter is required'}), 400

    # Obtenemos el parámetro 'top_k' de la URL osea cuantas recomendaciones va devolver
    # Si no se especifica, se usa el valor por defecto 5
    top_k = int(request.args.get('top_k', 5))

    # Buscamos la información de la película en el dataset
    info = reco.obtener_info_pelicula(titulo)

    # Si no se encuentra la película, devolvemos un error 404 (Not Found)
    if info is None:
        return jsonify({'error': f"Movie '{titulo}' not found"}), 404

    # Obtenemos las películas más similares usando el recomendador
    recs = reco.recomendar(titulo, top_k=top_k)

    # Retornamos la película base y sus recomendaciones en formato JSON
    return jsonify({'movie': info, 'recommendations': recs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
