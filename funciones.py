import unicodedata
import re
import comparar_frases as cf
import pandas as pd
import numpy as np

def normalizar_texto(texto):
    """
    Función completa para limpiar y estandarizar los nombres de las ciudades.
    """
    if not isinstance(texto, str):
        return ""
    
    # 1. Convertir a minúsculas
    texto = texto.lower()
    
    # 2. Eliminar acentos
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    
    # 3. Eliminar palabras comunes 
    stopwords = ['de', 'do', 'da', 'dos', 'das', 'municipio', 'e', 'o', 'a']
    # Usamos expresiones regulares para quitar palabras completas
    for stopword in stopwords:
        texto = re.sub(r'\b' + stopword + r'\b', '', texto)
        
    # 4. Eliminar caracteres no alfanuméricos y espacios extra
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto


def comparar_estados(df, gdf, nombres_norm = ['Estado_norm', 'Estado_norm']):
    comparaciones = []
    nombre_df = nombres_norm[0]
    nombre_gdf = nombres_norm[1]
    estados = gdf[nombre_gdf].unique()
    for idx, nombre_censo in enumerate(df[nombre_df].unique()):
        similitudes = np.array(cf.buscar_frase(nombre_censo, estados))
        max_sim = similitudes.max()
        indices_max = np.where(similitudes == max_sim)[0]
        comparaciones.append({
            'estado_censo': nombre_censo,
            'estado_gdf': estados[indices_max[0]] if indices_max.size == 1 else estados[indices_max],
            'similitud_estado': max_sim
            })

    tabla_comparativa = pd.DataFrame(comparaciones)
    return tabla_comparativa

def comparar_ciudades(df, gdf,tabla_Estados,estados_norm = ['Estado_norm', 'Estado_norm'], ciudades_norm = ['Ciudad_norm','Ciudad_norm']):
    estados_df = estados_norm[0]
    estados_gdf = estados_norm[1]

    nombre_df = ciudades_norm[0]
    nombre_gdf = ciudades_norm[1]
    
    comparaciones = []

    for c in range(len(tabla_Estados)):
        censo = df[df[estados_df] == tabla_Estados.iloc[c]['estado_censo']]
        geo = gdf[gdf[estados_gdf] == tabla_Estados.iloc[c]['estado_gdf']]
        ciudades = geo[nombre_gdf].unique()
        for idx, nombre_censo in enumerate(censo[nombre_df]):
            similitudes = np.array(cf.buscar_frase(nombre_censo, ciudades))
            max_sim = similitudes.max()
            indices_max = np.where(similitudes == max_sim)[0]
            comparaciones.append({
                'indice': idx,
                'Estado_censo': tabla_Estados.iloc[c]['estado_censo'],
                'nombre_censo': nombre_censo,
                'nombre_gdf': ciudades[indices_max[0]] if indices_max.size == 1 else ciudades[indices_max],
                'similitud': max_sim
                })

    tabla_comparativa = pd.DataFrame(comparaciones)
    return tabla_comparativa

    