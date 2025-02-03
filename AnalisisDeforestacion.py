import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df.columns = df.columns.str.strip().str.lower()  # Normalizar nombres de columnas
    return df

# Cargar datos
df = load_data()

# Convertir a GeoDataFrame
if "latitud" in df.columns and "longitud" in df.columns:
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitud"], df["latitud"]))
else:
    st.error("Las columnas 'latitud' y 'longitud' no se encuentran en el DataFrame. Verifica los nombres de las columnas.")

# Mostrar nombres de columnas para depuración
st.subheader("Nombres de columnas en el DataFrame")
st.write(df.columns.tolist())

# Título de la aplicación
st.title("Análisis de Deforestación")

# Vista previa de los datos
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# Mapa básico
st.subheader("Mapa de zonas deforestadas")

if "geometry" in gdf:
    mapa = folium.Map(location=[gdf["latitud"].mean(), gdf["longitud"].mean()], zoom_start=5)
    
    # Agregar puntos al mapa de forma vectorizada
    puntos = gdf[["latitud", "longitud"]].dropna().values.tolist()
    markers = [folium.CircleMarker(
        location=p,
        radius=3,
        color="red",
        fill=True,
        fill_color="red"
    ) for p in puntos]
    
    for marker in markers:
        marker.add_to(mapa)
    
    folium_static(mapa)
else:
    st.error("No se pudo generar el mapa debido a problemas con las coordenadas.")
