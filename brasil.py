#%%

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import comparar_frases as cf
#from thefuzz import process, fuzz
import unicodedata
import re


# %%
dire = r"D:\Bases de Datos\América"

df = pd.read_excel(dire+"/Amazonas.xlsx")
# %%
df.ADM0NAME.unique()
# %%
gdf = gpd.read_file(dire+"/BR_municipios_2024.zip")
# %%

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

df['Ciudad_norm'] = df['ADM2NAME'].apply(normalizar_texto)
gdf['Ciudad_norm'] = gdf['NM_MUN'].apply(normalizar_texto)
df['Estado_norm'] = df['ADM1NAME'].apply(normalizar_texto)
gdf['Estado_norm'] = gdf['NM_UF'].apply(normalizar_texto)
#%%

brasil = df[df.ADM0NAME == 'Brasil']

brasil

#%%
## Comparaciones de Estados
comparaciones = []
estados = gdf['NM_UF'].apply(normalizar_texto)
estados = estados.unique()

for idx, nombre_censo in enumerate(brasil['Estado_norm'].unique()):
    similitudes = np.array(cf.buscar_frase(nombre_censo, estados))
    max_sim = similitudes.max()
    indices_max = np.where(similitudes == max_sim)[0]
    comparaciones.append({
        'nombre_censo': nombre_censo,
        'nombre_gdf': estados[indices_max[0]] if indices_max.size == 1 else estados[indices_max],
        'similitud': max_sim
        })

tabla_comparativa = pd.DataFrame(comparaciones)
tabla_comparativa.head()
#%%
tabla_Estados = tabla_comparativa
# %%
brasil = pd.merge(brasil,tabla_comparativa, left_on='Estado_norm', right_on='nombre_censo')


#%%
comparaciones = []

for c in range(len(tabla_Estados)):
    censo = brasil[brasil['Estado_norm'] == tabla_Estados.iloc[c]['nombre_censo']]
    geo = gdf[gdf['Estado_norm'] == tabla_Estados.iloc[c]['nombre_gdf']]
    ciudades = geo.Ciudad_norm.unique()
    for idx, nombre_censo in enumerate(censo['Ciudad_norm']):
        similitudes = np.array(cf.buscar_frase(nombre_censo, ciudades))
        max_sim = similitudes.max()
        indices_max = np.where(similitudes == max_sim)[0]
        comparaciones.append({
            'indice': idx,
            'Estado_censo': tabla_Estados.iloc[c]['nombre_censo'],
            'nombre_censo': nombre_censo,
            'nombre_gdf': ciudades[indices_max[0]] if indices_max.size == 1 else ciudades[indices_max],
            'similitud': max_sim
            })

tabla_comparativa = pd.DataFrame(comparaciones)
tabla_comparativa.head()
# %%
tabla_comparativa[tabla_comparativa.similitud < 90]

# %%
tabla_comparativa
# %%
Brasil = pd.merge(brasil, tabla_comparativa, left_on = ['Estado_norm','Ciudad_norm'], right_on= ['Estado_censo','nombre_censo'])
# %%
Brasil 
# %%
amazonas = gpd.read_file(dire+"/Limites2024.zip")


unidades_en_amazonas = gpd.sjoin(gdf,amazonas, predicate='within')
unidades_en_amazonas
# %%

# %%
# Corrección del único nombre que lo empareja con dos, revisando hay mas coincidencia con el primero
Brasil.iloc[144, indice] = Brasil.iloc[1440].loc['nombre_gdf_y'][0]


Brasil = pd.merge(Brasil[Brasil.similitud_y >= 90]
         , unidades_en_amazonas.drop('geometry', axis = 1)
         , how = 'left', left_on = ['nombre_gdf_x','nombre_gdf_y']
         , right_on=['Estado_norm', 'Ciudad_norm'] , indicator = True )
# %%
Brasil['Amazonas'] = Brasil._merge == 'both'
Brasil.drop('_merge', axis = 1, inplace = True)

# %%
Brasil.to_csv("Brasil.csv")
# %%
