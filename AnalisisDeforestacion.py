import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import io
import zipfile
import pandas as pd
import os

# Función para cargar datos (con caché)
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

# URL del archivo zip del mapa del mundo
ruta_zip = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"

# Descargar y procesar el archivo zip (con manejo de errores)
try:
    response = requests.get(ruta_zip, stream=True)
    response.raise_for_status()

    with open("temp.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile("temp.zip", 'r') as z:
        shp_file = next((f for f in z.namelist() if f.endswith('.shp')), None)
        if shp_file:
            with z.open(shp_file) as f:
                mundo_dataframe = gpd.read_file(f)
        else:
            raise ValueError("No se encontró el archivo .shp dentro del archivo zip.")

    os.remove("temp.zip")

except requests.exceptions.RequestException as e:
    st.error(f"Error al descargar el mapa mundial: {e}")
    st.stop()
except (zipfile.BadZipFile, ValueError) as e:
    st.error(f"Error al procesar el archivo zip: {e}")
    st.stop()
except Exception as e:
    st.error(f"Un error inesperado ocurrió: {e}")
    st.stop()

# Cargar datos de deforestación
df = load_data(data_url)

if df is None:
    st.stop()

# Verificar columnas requeridas
required_columns = ["Latitud", "Longitud"]
if all(col in df.columns for col in required_columns):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]))

    # Título de la aplicación
    st.title("Análisis de Deforestación")

    # Vista previa de los datos
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # Mapa de zonas deforestadas
    st.subheader("Mapa de zonas deforestadas")

    # Crear el mapa (usando matplotlib y superponiendo mapas)
    fig, ax = plt.subplots(figsize=(10, 10))
    mundo_dataframe.plot(ax=ax, color='lightgray', edgecolor='black')
    gdf.plot(ax=ax, marker='o', color='red', markersize=10)

    # Mostrar el mapa en Streamlit
    st.pyplot(fig)

else:
    st.error(f"Las columnas {required_columns} no se encuentran en el DataFrame. Verifica los nombres de las columnas.")
    st.write(df.columns.tolist())
    st.stop()
