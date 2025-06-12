#%%
import numpy as np
import pandas as pd
import geopandas as gpd
from config import *
from funciones import *


# %%

df =  pd.read_excel(dire+"/Amazonas.xlsx")

#%%
gdf = gpd.read_file(dire+"/ecuador/nxcantones.shp")
gdf = gdf.to_crs(epsg=EPSG)
gdf
#%%
len(gdf.DPA_DESCAN.unique()), len(gdf.DPA_DESPRO.unique())
# %%
df['Ciudad_norm'] = df['ADM2NAME'].apply(normalizar_texto)
gdf['Ciudad_norm'] = gdf['DPA_DESCAN'].apply(normalizar_texto)
df['Estado_norm'] = df['ADM1NAME'].apply(normalizar_texto)
gdf['Estado_norm'] = gdf['DPA_DESPRO'].apply(normalizar_texto)


# %%
ecuador = df[df.ADM0NAME == 'Ecuador']
ecuador

# %%
tabla_estados = comparar_estados(ecuador,gdf)
tabla_estados
# %%
# Eliminamos los estados que vienen del censo que son Santo Domingo y Santa Elena que no tienen georeferencia
tabla_estados = tabla_estados[tabla_estados.similitud_estado == 100]
ecuador = pd.merge(ecuador, tabla_estados, left_on='Estado_norm', right_on='estado_censo')
# %%

tabla_comparativa = comparar_ciudades(ecuador, gdf, tabla_estados)
tabla_comparativa
# %%
tabla_comparativa[tabla_comparativa.similitud >= 90]
# %%
tabla_comparativa[tabla_comparativa.similitud < 90]
# %%
ecuador = pd.merge(ecuador, tabla_comparativa, left_on=['Estado_norm','Ciudad_norm'],right_on= ['Estado_censo','nombre_censo'])
ecuador
# %%
amazonas = gpd.read_file(dire+"/Limites2024.zip")
amazonas = amazonas.to_crs(EPSG)
unidades_en_amazonas = gpd.sjoin(gdf,amazonas, predicate='within')
unidades_en_amazonas.plot()

# %%
Ecuador = pd.merge(ecuador[ecuador.similitud >= 90]
         , unidades_en_amazonas.drop('geometry', axis = 1)
         , how = 'left', left_on = ['estado_gdf','nombre_gdf']
         , right_on=['Estado_norm', 'Ciudad_norm'] , indicator = True )

# %%
Ecuador['Amazonas'] = Ecuador._merge == 'both'
Ecuador.drop('_merge', axis = 1, inplace = True)
# %%
Ecuador.to_csv(dire_guardado+'Ecuador.csv')

# %%
