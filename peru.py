
#%%
import numpy as np
import pandas as pd
import geopandas as gpd
from config import *
from funciones import *


# %%

df =  pd.read_excel(dire+"/Amazonas.xlsx")

#%%
gdf = gpd.read_file(dire+"/DISTRITOS_peru.zip")
gdf = gdf.to_crs(epsg=EPSG)
gdf
#%%
len(gdf.NOMBDEP.unique()), len(gdf.NOMBPROV.unique())
# %%
df['Ciudad_norm'] = df['ADM2NAME'].apply(normalizar_texto)
gdf['Ciudad_norm'] = gdf['NOMBPROV'].apply(normalizar_texto)
df['Estado_norm'] = df['ADM1NAME'].apply(normalizar_texto)
gdf['Estado_norm'] = gdf['NOMBDEP'].apply(normalizar_texto)


# %%
peru = df[df.ADM0NAME == 'Peru']
peru

# %%
tabla_estados = comparar_estados(peru,gdf)
tabla_estados
#%%
# Eliminamos los estados que vienen del censo que no tienen georeferencia o no se encuentra la ciduda

tabla_estados.iloc[-1,1] = tabla_estados.iloc[-1].estado_gdf[1]
tabla_estados = tabla_estados.drop(0)

#%%
peru = pd.merge(peru, tabla_estados, left_on='Estado_norm', right_on='estado_censo')
# %%

tabla_comparativa = comparar_ciudades(peru, gdf, tabla_estados)
tabla_comparativa
# %%
tabla_comparativa[tabla_comparativa.similitud >= 90]
# %%
tabla_comparativa[tabla_comparativa.similitud < 90]
# %%
peru = pd.merge(peru, tabla_comparativa, left_on=['Estado_norm','Ciudad_norm'],right_on= ['Estado_censo','nombre_censo'])
peru
# %%
amazonas = gpd.read_file(dire+"/Limites2024.zip")
amazonas = amazonas.to_crs(EPSG)
unidades_en_amazonas = gpd.sjoin(gdf,amazonas, predicate='within')
unidades_en_amazonas.plot()

# %%
Peru = pd.merge(peru[peru.similitud >= 90]
         , unidades_en_amazonas.drop('geometry', axis = 1)
         , how = 'left', left_on = ['estado_gdf','nombre_gdf']
         , right_on=['Estado_norm', 'Ciudad_norm'] , indicator = True )

# %%
Peru['Amazonas'] = Peru._merge == 'both'
Peru.drop('_merge', axis = 1, inplace = True)
# %%
Peru.to_csv(dire_guardado+'Peru.csv')

# %%
