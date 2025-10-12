import pandas as pd                                          # Para manejo de datasets
from sklearn.feature_extraction.text import TfidfVectorizer  # Para convertir texto en vectores TF-IDF
from sklearn.metrics.pairwise import linear_kernel           # Para calcular similitud coseno entre vectores

class Recomendador:
    #Se inicializa el recomendador cargando los datos y preparando los vectores
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv                  
        self.datos = pd.read_csv(ruta_csv)        

        # Creamos una columna combinada que unifica la información textual de cada película
        self.datos['combinado'] = (
            self.datos['title'].fillna('') + ' ' +       
            self.datos['genres'].fillna('') + ' ' +      
            self.datos['actors'].fillna('') + ' ' +     
            self.datos['director'].fillna('')            
        )

        # Guardamos los títulos como lista para mostrar los resultados
        self.titulos = self.datos['title'].astype(str).tolist()

        # Creamos un vectorizador TF-IDF que eliminará palabras vacías del inglés
        self.vectorizador = TfidfVectorizer(stop_words='english')

        # Convertimos el texto combinado en una matriz TF-IDF
        # Cada fila representa una película y cada columna una palabra ponderada
        self.matriz_tfidf = self.vectorizador.fit_transform(self.datos['combinado'])

        # Calculamos la matriz de similitud coseno entre todas las películas
        # Cada valor [i][j] representa que tan similares son las películas i y j
        self.similitud_coseno = linear_kernel(self.matriz_tfidf, self.matriz_tfidf)

        # Creamos un diccionario que mapea título a índice de la película
        self.titulo_a_indice = {title: idx for idx, title in enumerate(self.datos['title'].astype(str))}

    # Método para listar todas las películas con sus datos principales
    def listar_peliculas(self):
         # Columnas que queremos mostrar
        cols = ['title', 'genres', 'actors', 'director']  
        for c in cols:
            # Si alguna falta, la agregamos vacía
            if c not in self.datos.columns:               
                self.datos[c] = ''
        # Convertimos las columnas seleccionadas a una lista de diccionarios
        registros = self.datos[cols].fillna('').to_dict(orient='records')
        return registros

    # Método para obtener la información de una película específica por su título
    def obtener_info_pelicula(self, titulo):
        #Buscamos el índice asociado al título y si no existe se retorna None
        idx = self.titulo_a_indice.get(titulo)  
        if idx is None:                         
            return None
        # Obtenemos la fila correspondiente
        fila = self.datos.iloc[idx]             
        # Retornamos la información como diccionario
        return {
            'title': fila['title'],
            'genres': fila.get('genres', ''),
            'actors': fila.get('actors', ''),
            'director': fila.get('director', '')
        }

    def recomendar(self, titulo, top_k=5):
        # Genera una lista de las películas más similares al título dado
        # Buscamos el índice de la película y si no esta en el dataset se devuelve una lista vacia
        idx = self.titulo_a_indice.get(titulo)  
        if idx is None:                         
            return []

        # Obtenemos los puntajes de similitud de esa película con todas las demás
        sim_scores = list(enumerate(self.similitud_coseno[idx]))

        # Excluimos la película original pa que no se recomiende a si misma
        sim_scores = [(i, score) for i, score in sim_scores if i != idx]

        # Ordenamos las películas según el puntaje de similitud (de mayor a menor)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Creamos la lista final de recomendaciones
        recomendaciones = []
        for i, score in sim_scores[:top_k]:  # Tomamos las "top_k" más similares
            fila = self.datos.iloc[i]
            recomendaciones.append({
                'title': fila['title'],
                'genres': fila.get('genres', ''),
                'actors': fila.get('actors', ''),
                'director': fila.get('director', ''),
                'score': float(score)  # Convertimos el puntaje a un float legible
            })
        return recomendaciones

