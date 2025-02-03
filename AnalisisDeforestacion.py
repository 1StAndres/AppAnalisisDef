import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from shapely.geometry import Point
import requests
import zipfile
import io

# Cargar datos
url_csv = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
csv_data = pd.read_csv(url_csv)

# Convertir las coordenadas a un objeto GeoDataFrame
geometry = [Point(xy) for xy in zip(csv_data['Longitud'], csv_data['Latitud'])]
gdf_deforestacion = gpd.GeoDataFrame(csv_data, geometry=geometry)

# Cargar el mapa base de países
url_shapefile = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
r = requests.get(url_shapefile)
with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
    zip_ref.extractall("ne_50m_admin_0_countries")

gdf_world = gpd.read_file("ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp")

# Función para filtrar datos según los rangos seleccionados
def filtrar_datos(rangos):
    df_filtrado = gdf_deforestacion.copy()
    for columna, (min_val, max_val) in rangos.items():
        df_filtrado = df_filtrado[(df_filtrado[columna] >= min_val) & (df_filtrado[columna] <= max_val)]
    return df_filtrado

# Función para el análisis de clústeres
def analisis_clusters(df):
    kmeans = KMeans(n_clusters=3)
    df['Cluster'] = kmeans.fit_predict(df[['Superficie_Deforestada', 'Altitud']])
    return df

# Función para mostrar el gráfico de torta
def grafico_torta(df):
    vegetacion_counts = df['Tipo_Vegetacion'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(vegetacion_counts, labels=vegetacion_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Aplicación Streamlit
st.title('Análisis de Datos de Deforestación')

# Selección de variables para filtrar
variables = ['Latitud', 'Longitud', 'Superficie_Deforestada', 'Tasa_Deforestacion', 
             'Tipo_Vegetacion', 'Altitud', 'Pendiente', 'Distancia_Carretera', 
             'Precipitacion', 'Temperatura']

rangos = {}
for var in variables:
    min_val = float(st.number_input(f'Valor mínimo de {var}', value=float(csv_data[var].min())))
    max_val = float(st.number_input(f'Valor máximo de {var}', value=float(csv_data[var].max())))
    rangos[var] = (min_val, max_val)

# Filtrar datos según los rangos seleccionados
df_filtrado = filtrar_datos(rangos)

# Mostrar mapa de deforestación filtrado
st.subheader('Mapa de deforestación filtrado')
gdf_deforestacion_filtrado = gpd.GeoDataFrame(df_filtrado, geometry=gdf_deforestacion.geometry)
ax = gdf_world.plot(figsize=(10, 10), color='lightgrey')
gdf_deforestacion_filtrado.plot(ax=ax, marker='o', color='red', markersize=5)
st.pyplot(fig)

# Análisis de clústeres
st.subheader('Análisis de clústeres')
df_clusters = analisis_clusters(df_filtrado)
st.write(df_clusters[['Latitud', 'Longitud', 'Cluster']].head())

# Mostrar gráfico de torta
st.subheader('Gráfico de torta según tipo de vegetación')
grafico_torta(df_filtrado)
