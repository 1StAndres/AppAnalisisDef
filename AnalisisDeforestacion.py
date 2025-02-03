import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    return df

# Cargar datos
df = load_data()

# Convertir a GeoDataFrame
if "Latitud" in df.columns and "Longitud" in df.columns:
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]))
else:
    st.error("Las columnas 'Latitud' y 'Longitud' no se encuentran en el DataFrame. Verifica los nombres de las columnas.")

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
    mapa = folium.Map(location=[gdf["Latitud"].mean(), gdf["Longitud"].mean()], zoom_start=5)
    
    # Agregar puntos al mapa sin usar bucles explícitos
    feature_group = folium.FeatureGroup(name="Deforestación")
    gdf.apply(lambda row: feature_group.add_child(
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,
            color="red",
            fill=True,
            fill_color="red"
        )
    ), axis=1)
    
    mapa.add_child(feature_group)
    folium_static(mapa)
else:
    st.error("No se pudo generar el mapa debido a problemas con las coordenadas.")
