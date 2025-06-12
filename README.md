# amazonas
detecta las ciudades que están en amazonía

# Proyecto Amazonía

Este proyecto analiza y compara datos censales y geográficos de la región amazónica de varios países sudamericanos utilizando Python, pandas y geopandas.

## Estructura del Proyecto

```
amazonas.csv
bolivia.py
brasil.py
colombia.py
comparar_frases.py
config.py
datos_final.ipynb
ecuador.py
funciones.py
localizar.ipynb
peru.py
revisión_datos.ipynb
venezuela.py
dfs/
    bolivia.csv
    Brasil.csv
    Colombia.csv
    Ecuador.csv
    Peru.csv
    venezuela.csv
```

- **Archivos `.py`**: Scripts para procesar y analizar datos de cada país.
- **`revisión_datos.ipynb`**: Notebook principal de análisis y visualización.
- **`dfs/`**: Datos censales procesados por país.
- **`config.py`**: Configuración de variables y columnas de interés.

## Requisitos

- Python 3.10+
- pandas
- geopandas
- matplotlib
- numpy

Instala las dependencias con:

```sh
pip install pandas geopandas matplotlib numpy
```

## Uso

1. **Configura las rutas de datos**  
   Modifica la variable `dire` en los notebooks y scripts para que apunte a la carpeta donde tienes los archivos de datos.

2. **Ejecuta los notebooks**  
   Abre [revisión_datos.ipynb](revisión_datos.ipynb) en Jupyter o VSCode para explorar el análisis y las visualizaciones.

3. **Procesamiento por país**  
   Puedes ejecutar los scripts individuales (por ejemplo, [ecuador.py](ecuador.py), [peru.py](peru.py)) para procesar datos específicos de cada país.

## Ejemplo de uso

Carga y visualiza límites municipales de Brasil:

````python
import geopandas as gpd
dire = r"D:\Bases de Datos\América"
gdf = gpd.read_file(dire + "/BR_municipios_2024.zip")
gdf.boundary.plot()
