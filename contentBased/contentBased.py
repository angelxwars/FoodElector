import pandas as pd
#import stop_words as stopwords
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np


class ContentBased(object):
    """
    Modelo de recomendación de recetas basado en ingredientes.
    Vectorizamos cada receta para conocer las mas cercanas
    """

    def __init__(self, stop_words=None, token_pattern=None, metric='cosine', n_neighbors=5):

        if token_pattern is None:
            token_pattern = '(?u)\\b[a-zA-Z]\\w\\w+\\b'

        self.tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=token_pattern)
        self.nearest_neigbors = NearestNeighbors(metric=metric, n_neighbors=n_neighbors, algorithm='brute')

    def fit(self, datos, columna_descripcion):
        """
        Entrenamos el modelo:
        1- Vectorizamos cada receta
        2- Calculamos las recetas mas cercanos
        """
        self.datos = datos
        datos_por_tags = self.tfidf_vectorizer.fit_transform(datos[columna_descripcion].values.astype('U'))
        self.nearest_neigbors.fit(datos_por_tags)

    def predict(self, descripcion):
        """
        Devolverá la receta que mas parecida sea en la cadena de ingredientes
        """
        descripcion_tags = self.tfidf_vectorizer.transform(descripcion)
        if descripcion_tags.sum() == 0:
            return pd.DataFrame(columns=self.datos.columns)
        else:
            _, indices = self.nearest_neigbors.kneighbors(descripcion_tags)


        return self.datos.iloc[indices[0], :]