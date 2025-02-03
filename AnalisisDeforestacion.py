import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import io
import zipfile
import pandas as pd  # Importa pandas aquí

# Definir la función load_data *antes* de usarla
@st.cache_data  # Para mejorar el rendimiento
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")  # Usa st.error para mostrar el error en Streamlit
        return None

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

# URL del archivo zip del mapa del mundo
ruta_zip = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"

# Descargar el archivo zip
try:  # Manejar posibles errores de descarga
    response = requests.get(ruta_zip, stream=True)
    response.raise_for_status()  # Lanza una excepción si la descarga falla
except requests.exceptions.RequestException as e:
    st.error(f"Error al descargar el mapa mundial: {e}")
    st.stop()  # Detener la ejecución si falla la descarga

# Descomprimir el archivo zip en memoria
try:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Buscar el archivo .shp (podría haber otros)
        shp_file = next((f for f in z.namelist() if f.endswith('.shp')), None)
        if shp_file:
            with z.open(shp_file) as f:
                mundo_dataframe = gpd.read_file(f)
        else:
            raise ValueError("No se encontró el archivo .shp dentro del archivo zip.")
except (zipfile.BadZipFile, ValueError) as e:  # Captura errores de zip
    st.error(f"Error al procesar el archivo zip: {e}")
    st.stop()


# Cargar datos de deforestación
df = load_data(data_url)

if df is None:
    st.stop()  # Detener la ejecución si no se cargan los datos

# Check for required columns
required_columns = ["Latitud", "Longitud"]
if all(col in df.columns for col in required_columns):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]))

    st.title("Análisis de Deforestación")  # Título de la app

    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    st.subheader("Mapa de zonas deforestadas")

    # Crear el mapa base con el mapa del mundo
    fig, ax = plt.subplots(figsize=(10, 10))
    mundo_dataframe.plot(ax=ax, color='lightgray', edgecolor='black')

    # Superponer los puntos de deforestación
    gdf.plot(ax=ax, marker='o', color='red', markersize=10)

    st.pyplot(fig)  # Mostrar el mapa en Streamlit

else:
    st.error(f"Las columnas {required_columns} no se encuentran en el DataFrame. Verifica los nombres de las columnas.")
    st.write(df.columns.tolist())  # Mostrar las columnas disponibles para depuración
    st.stop()
