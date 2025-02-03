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

# Función para mostrar el análisis de datos de deforestación
def analisis_deforestacion(gdf):
    st.subheader("Análisis de Deforestación")
    
    # Cálculo de superficie deforestada total
    superficie_total = gdf['Superficie_Deforestada'].sum()
    st.write(f"Superficie total deforestada: {superficie_total} hectáreas")
    
    # Cálculo de tasa de deforestación promedio
    tasa_promedio = gdf['Tasa_Deforestacion'].mean()
    st.write(f"Tasa promedio de deforestación: {tasa_promedio}%")
    
    # Visualización de resumen de las columnas relevantes
    st.write("Resumen de las primeras filas del dataset:")
    st.write(gdf[['Fecha', 'Superficie_Deforestada', 'Tasa_Deforestacion', 'Tipo_Vegetacion', 'Altitud']].head())

# Función para mostrar el mapa según la variable seleccionada
def mostrar_mapa(gdf):
    st.subheader("Visualizar mapa de zonas deforestadas")
    
    # Selección de variable para el mapa
    variable = st.selectbox("Selecciona la variable para visualizar en el mapa", gdf.columns.to_list())
    
    # Inicializamos el mapa centrado en un punto aproximado
    m = folium.Map(location=[gdf['Latitud'].mean(), gdf['Longitud'].mean()], zoom_start=6)
    
    # Función para asignar color a los puntos según el valor de la variable
    def asignar_color(valor, variable):
        if variable == "Tipo_Vegetacion":
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
        elif variable == "Precipitacion":
            # Asignar color según la precipitación
            if valor < 1000:
                return "blue"
            elif valor < 2000:
                return "yellow"
            else:
                return "red"
        elif variable == "Superficie_Deforestada":
            # Asignar color según la superficie deforestada (Ejemplo: más rojo para más deforestación)
            if valor < 50:
                return "green"
            elif valor < 100:
                return "orange"
            else:
                return "red"
    
    # Añadir los puntos al mapa
    for idx, row in gdf.iterrows():
        try:
            color = asignar_color(row[variable], variable)
            folium.CircleMarker(
                location=[row['Latitud'], row['Longitud']],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
            ).add_to(m)
        except KeyError:
            st.error(f"La columna '{variable}' no existe en los datos.")
            return
    
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

        # Realizar análisis de deforestación
        analisis_deforestacion(gdf)

        # Mostrar el mapa con las zonas deforestadas
        mostrar_mapa(gdf)

# Ejecutar la app
if __name__ == "__main__":
    main()

