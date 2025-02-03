import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data(data_url)

if df is None:  # Stop execution if data loading failed
    st.stop()

# Check for required columns *after* loading the data
required_columns = ["Latitud", "Longitud"]
if all(col in df.columns for col in required_columns):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]))

    # Now that the data is loaded and columns are checked, set the title
    st.title("Análisis de Deforestación")

    # ... (rest of your Streamlit code)

    # Vista previa de los datos
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # Mapa básico
    st.subheader("Mapa de zonas deforestadas")

    if "geometry" in gdf:
        mapa = folium.Map(location=[gdf["Latitud"].mean(), gdf["Longitud"].mean()], zoom_start=5)

        # Agregar puntos al mapa sin usar bucles explícitos (improved)
        for _, row in gdf.iterrows():  # More efficient than apply for this case
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=3,
                color="red",
                fill=True,
                fill_color="red"
            ).add_to(mapa)

        folium_static(mapa)
    else:
        st.error("No se pudo generar el mapa debido a problemas con las coordenadas.")

else:
    st.error(f"Las columnas {required_columns} no se encuentran en el DataFrame. Verifica los nombres de las columnas.")
    st.write(df.columns.tolist()) # Show available columns for debugging
    st.stop() # Stop execution if columns are missing
