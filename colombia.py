#%%
import numpy as np
import pandas as pd
import geopandas as gpd
from config import *
from funciones import *


# %%

df =  pd.read_excel(dire+"/Amazonas.xlsx")

#%%
gdf = gpd.read_file(dire+"/colombia/colombia.shp")
gdf.drop('geometry', axis= 1, inplace=True)
gdf =  gpd.GeoDataFrame(gdf, geometry = gpd.points_from_xy(gdf.longitud,gdf.latitud ))

gdf.crs = 4326
gdf = gdf.to_crs(EPSG)
gdf
#%%
len(gdf.estado.unique()), len(gdf.ciudad.unique())
# %%
df['Ciudad_norm'] = df['ADM2NAME'].apply(normalizar_texto)
gdf['Ciudad_norm'] = gdf['ciudad'].apply(normalizar_texto)
df['Estado_norm'] = df['ADM1NAME'].apply(normalizar_texto)
gdf['Estado_norm'] = gdf['estado'].apply(normalizar_texto)


# %%
colombia = df[df.ADM0NAME == 'Colombia']
colombia

# %%
tabla_estados = comparar_estados(colombia,gdf)
tabla_estados
# %%
# Eliminamos los estados que vienen del censo que son Santo Domingo y Santa Elena que no tienen georeferencia
tabla_estados = tabla_estados[tabla_estados.similitud_estado == 100]
colombia = pd.merge(colombia, tabla_estados, left_on='Estado_norm', right_on='estado_censo')
# %%

tabla_comparativa = comparar_ciudades(colombia, gdf, tabla_estados)
tabla_comparativa
# %%
tabla_comparativa[tabla_comparativa.similitud >= 90]
# %%
tabla_comparativa[tabla_comparativa.similitud < 90]
# %%
colombia = pd.merge(colombia, tabla_comparativa, left_on=['Estado_norm','Ciudad_norm'],right_on= ['Estado_censo','nombre_censo'])
colombia
# %%
amazonas = gpd.read_file(dire+"/Limites2024.zip")
amazonas = amazonas.to_crs(EPSG)
unidades_en_amazonas = gpd.sjoin(gdf,amazonas, predicate='within')
unidades_en_amazonas.plot()

# %%
colombia = pd.merge(colombia[colombia.similitud >= 90]
         , unidades_en_amazonas.drop('geometry', axis = 1)
          , how = 'left', left_on = ['estado_gdf','nombre_gdf']
         , right_on=['Estado_norm', 'Ciudad_norm'] , indicator = True )

# %%
colombia['Amazonas'] = colombia._merge == 'both'
colombia.drop('_merge', axis = 1, inplace = True)
# %%
colombia.to_csv(dire_guardado+'Colombia.csv')
# %%
