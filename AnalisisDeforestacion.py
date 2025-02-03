import geopandas as gpd
import folium
import streamlit as st
import pandas as pd
from folium.plugins import HeatMap

# Función para cargar los datos usando GeoPandas
def cargar_datos():
    opcion = st.selectbox("¿Cómo te gustaría cargar los datos?", ["Subir archivo CSV", "Leer desde URL"])
    
    if opcion == "Subir archivo CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            # Cargar el archivo CSV con latitud y longitud
            df = pd.read_csv(archivo)
            # Convertir a GeoDataFrame usando las columnas de latitud y longitud
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitud'], df['Latitud']))
            return gdf
    
    elif opcion == "Leer desde URL":
        url = st.text_input("Introduce la URL del archivo CSV")
        if url:
            # Leer el archivo CSV directamente desde la URL
            df = pd.read_csv(url)
            # Convertir a GeoDataFrame
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitud'], df['Latitud']))
            return gdf

    return None

# Función para mostrar el mapa según la variable seleccionada
def mostrar_mapa(gdf):
    st.subheader("Visualizar mapa de zonas deforestadas")
    
    # Selección de variable para el mapa
    variable = st.selectbox("Selecciona la variable para visualizar en el mapa", ["Tipo de Vegetación", "Altitud", "Precipitación"])
    
    # Inicializamos el mapa centrado en un punto aproximado
    m = folium.Map(location=[gdf['Latitud'].mean(), gdf['Longitud'].mean()], zoom_start=6)
    
    # Función para asignar color a los puntos según el valor de la variable
    def asignar_color(valor, variable):
        if variable == "Tipo de Vegetación":
            # Asignar un color basado en el tipo de vegetación
            colores = {"Bosque": "green", "Selva": "darkgreen", "Pastizales": "yellow", "Desierto": "brown"}
            return colores.get(valor, "gray")
        elif variable == "Altitud":
            # Asignar color según la altitud
            if valor < 1000:
                return "blue"
            elif valor < 2000:
                return "orange"
            else:
                return "red"
        elif variable == "Precipitación":
            # Asignar color según la precipitación
            if valor < 1000:
                return "blue"
            elif valor < 2000:
                return "yellow"
            else:
                return "red"
    
    # Añadir los puntos al mapa
    for idx, row in gdf.iterrows():
        color = asignar_color(row[variable], variable)
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(m)
    
    # Mostrar el mapa
    st.markdown("### Mapa de Zonas Deforestadas")
    st.write(m)

# Función principal para la app
def main():
    st.title("Análisis de Deforestación")
    
    # Cargar los datos
    gdf = cargar_datos()
    
    if gdf is not None:
        # Mostrar los datos originales
        st.subheader("Vista previa de los datos")
        st.write(gdf.head())

        # Mostrar el mapa con las zonas deforestadas
        mostrar_mapa(gdf)

# Ejecutar la app
if __name__ == "__main__":
    main()
