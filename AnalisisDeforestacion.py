import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from shapely.geometry import Point

# Cargar el archivo CSV desde la URL proporcionada
url = 'https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv'
df = pd.read_csv(url)

# Interpolación de valores faltantes
df = df.interpolate(method='linear', axis=0)

# Convertir el DataFrame a GeoDataFrame usando las coordenadas de Latitud y Longitud
geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Establecer el CRS (sistema de referencia de coordenadas)
gdf.set_crs("EPSG:4326", inplace=True)

# Análisis de clústeres de superficies deforestadas
X = df[['Latitud', 'Longitud', 'Superficie_Deforestada']].dropna()
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
df['Cluster'] = kmeans.labels_

# Función para generar mapas interactivos con Folium
def generar_mapa_folium(gdf, color='red'):
    mapa = folium.Map(location=[gdf['Latitud'].mean(), gdf['Longitud'].mean()], zoom_start=6)
    for _, row in gdf.iterrows():
        folium.CircleMarker(location=[row['Latitud'], row['Longitud']], radius=5, color=color, fill=True, fill_color=color, fill_opacity=0.6).add_to(mapa)
    return mapa

# Mostrar mapas de zonas deforestadas con GeoPandas
st.subheader("Mapa de Zonas Deforestadas por Tipo de Vegetación")
mapa_vegetacion = generar_mapa_folium(gdf[gdf['Tipo_Vegetacion'].notnull()], color='red')
st.write(mapa_vegetacion)

st.subheader("Mapa de Zonas Deforestadas por Altitud")
mapa_altitud = generar_mapa_folium(gdf[gdf['Altitud'].notnull()], color='blue')
st.write(mapa_altitud)

st.subheader("Mapa de Zonas Deforestadas por Precipitación")
mapa_precipitacion = generar_mapa_folium(gdf[gdf['Precipitacion'].notnull()], color='green')
st.write(mapa_precipitacion)

# Gráfico de torta de tipos de vegetación
st.subheader("Gráfico de Torta según Tipo de Vegetación")
tipo_vegetacion_counts = df['Tipo_Vegetacion'].value_counts()

fig, ax = plt.subplots()
ax.pie(tipo_vegetacion_counts, labels=tipo_vegetacion_counts.index, autopct='%1.1f%%', startangle=90, colors=['red', 'green', 'blue', 'orange', 'purple'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Filtros personalizados del usuario
st.sidebar.header("Filtros Personalizados")
variables = ['Latitud', 'Longitud', 'Altitud', 'Pendiente', 'Distancia_Carretera', 'Precipitacion', 'Temperatura']
seleccionadas = st.sidebar.multiselect("Selecciona hasta cuatro variables", variables, max_selections=4)

# Recoger los valores de los sliders para cada variable
filtros = {}
for var in seleccionadas:
    min_val = df[var].min()
    max_val = df[var].max()
    filtros[var] = st.sidebar.slider(f"Selecciona rango para {var}", min_val, max_val, (min_val, max_val))

# Aplicar los filtros y mostrar el mapa personalizado
if seleccionadas:
    df_filtrado = df
    for var, (min_val, max_val) in filtros.items():
        df_filtrado = df_filtrado[(df_filtrado[var] >= min_val) & (df_filtrado[var] <= max_val)]

    # Mostrar el mapa filtrado
    if not df_filtrado.empty:
        st.subheader("Mapa Personalizado según los filtros")
        mapa_personalizado = generar_mapa_folium(df_filtrado, 'orange')
        st.write(mapa_personalizado)
    else:
        st.write("No hay datos que coincidan con los filtros seleccionados.")
