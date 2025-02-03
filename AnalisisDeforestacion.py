import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
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

# Función para filtrar datos sin usar ciclos
def filtrar_datos(df, rangos):
    # Crear la máscara booleana inicial con True (sin ciclo)
    mask = (df[variables] >= pd.Series([rangos[var][0] for var in variables], index=variables)) & (df[variables] <= pd.Series([rangos[var][1] for var in variables], index=variables))
    return df[mask.all(axis=1)]

# Función para el análisis de clústeres
def analisis_clusters(df):
    df_cluster = df[['Superficie_Deforestada', 'Altitud']].dropna()
    kmeans = KMeans(n_clusters=3)
    df_cluster['Cluster'] = kmeans.fit_predict(df_cluster)
    return df_cluster

# Función para mostrar el gráfico de torta
def grafico_torta(df):
    vegetacion_counts = df['Tipo_Vegetacion'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(vegetacion_counts, labels=vegetacion_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Función para obtener min y max de las columnas numéricas
def obtener_min_max(df, var):
    return df[var].min(), df[var].max()

# Aplicación Streamlit
st.title('Análisis de Datos de Deforestación')

# Selección de variables para filtrar
variables = ['Latitud', 'Longitud', 'Superficie_Deforestada', 'Tasa_Deforestacion', 
             'Tipo_Vegetacion', 'Altitud', 'Pendiente', 'Distancia_Carretera', 
             'Precipitacion', 'Temperatura']

# Obtener rangos para cada variable sin usar ciclo
min_vals = pd.Series([obtener_min_max(csv_data, var)[0] for var in variables], index=variables)
max_vals = pd.Series([obtener_min_max(csv_data, var)[1] for var in variables], index=variables)

# Solicitar a los usuarios los valores de mínimo y máximo
rangos = pd.DataFrame({
    'min': min_vals,
    'max': max_vals
})

# Los valores proporcionados por el usuario
rangos['min'] = rangos['min'].apply(lambda x: st.number_input(f'Valor mínimo de {x.name}', value=x))
rangos['max'] = rangos['max'].apply(lambda x: st.number_input(f'Valor máximo de {x.name}', value=x))

# Filtrar datos según los rangos seleccionados
df_filtrado = filtrar_datos(gdf_deforestacion, rangos.to_dict(orient='index'))

# Mostrar mapa de deforestación filtrado
st.subheader('Mapa de deforestación filtrado')
gdf_deforestacion_filtrado = gpd.GeoDataFrame(df_filtrado, geometry=gdf_deforestacion.geometry)
ax = gdf_world.plot(figsize=(10, 10), color='lightgrey')
gdf_deforestacion_filtrado.plot(ax=ax, marker='o', color='red', markersize=5)
st.pyplot(fig)

# Análisis de clústeres
st.subheader('Análisis de clústeres')
df_clusters = analisis_clusters(df_filtrado)
st.write(df_clusters[['Superficie_Deforestada', 'Altitud', 'Cluster']].head())

# Mostrar gráfico de torta
st.subheader('Gráfico de torta según tipo de vegetación')
grafico_torta(df_filtrado)
