#%%
import numpy as np
import pandas as pd
import geopandas as gpd
from config import *
from funciones import *


# %%

df =  pd.read_excel(dire+"/Amazonas.xlsx")

#%%
gdf = gpd.read_file(dire+"/venezuela/venezuela.shp")
#gdf.drop('geometry', axis= 1, inplace=True)
#gdf =  gpd.GeoDataFrame(gdf, geometry = gpd.points_from_xy(gdf.longitud,gdf.latitud ))

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
venezuela = df[df.ADM0NAME == 'Venezuela']
venezuela

# %%
tabla_estados = comparar_estados(venezuela,gdf)
tabla_estados
# %%
# Eliminamos los estados que vienen del censo que son Santo Domingo y Santa Elena que no tienen georeferencia
tabla_estados = tabla_estados[tabla_estados.similitud_estado == 100]
venezuela = pd.merge(venezuela, tabla_estados, left_on='Estado_norm', right_on='estado_censo')
# %%

tabla_comparativa = comparar_ciudades(venezuela, gdf, tabla_estados)
tabla_comparativa
# %%
tabla_comparativa[tabla_comparativa.similitud >= 90]
# %%
tabla_comparativa[tabla_comparativa.similitud < 90]
# %%
venezuela = pd.merge(venezuela, tabla_comparativa, left_on=['Estado_norm','Ciudad_norm'],right_on= ['Estado_censo','nombre_censo'])
venezuela
# %%
amazonas = gpd.read_file(dire+"/Limites2024.zip")
amazonas = amazonas.to_crs(EPSG)
unidades_en_amazonas = gpd.sjoin(gdf,amazonas, predicate='within')
unidades_en_amazonas.plot()

# %%
venezuela = pd.merge(venezuela[venezuela.similitud >= 90]
         , unidades_en_amazonas.drop('geometry', axis = 1)
          , how = 'left', left_on = ['estado_gdf','nombre_gdf']
         , right_on=['Estado_norm', 'Ciudad_norm'] , indicator = True )

# %%
venezuela['Amazonas'] = venezuela._merge == 'both'
venezuela.drop('_merge', axis = 1, inplace = True)
# %%
venezuela.to_csv(dire_guardado+'/venezuela.csv')
# %%
