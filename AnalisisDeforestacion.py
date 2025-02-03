import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    return df

# Cargar datos
df = load_data()

# Título de la aplicación
st.title("Análisis de Deforestación")

# Vista previa de los datos
st.subheader("Vista previa de los datos")
st.dataframe(df.head())

# Mapa básico
st.subheader("Mapa de zonas deforestadas")
mapa = folium.Map(location=[df["Latitud"].mean(), df["Longitud"].mean()], zoom_start=5)

data = df[["Latitud", "Longitud"]].dropna().values.tolist()
folium.FeatureGroup(name="Deforestación").add_child(
    folium.plugins.MarkerCluster(locations=data, popups=df["tipo_vegetacion"].tolist())
).add_to(mapa)

folium_static(mapa)
