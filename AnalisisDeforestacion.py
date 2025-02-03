import streamlit as st
import pandas as pd
import folium

# Cargar los datos desde la URL
url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
df = pd.read_csv(url)

# Mostrar los primeros registros para confirmar que los datos se cargaron correctamente
st.write(df.head())

# Función para generar un mapa de deforestación según un campo
def mapa_deforestacion(df, columna, color='red'):
    # Filtrar los datos según el campo
    mapa = folium.Map(location=[df['Latitud'].mean(), df['Longitud'].mean()], zoom_start=6)
    
    # Agregar todos los puntos al mapa usando la columna seleccionada
    folium.CircleMarker(
        location=[df['Latitud'], df['Longitud']],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6
    ).add_to(mapa)
    
    return mapa

# Mapas de las zonas deforestadas por tipo de vegetación
st.subheader("Mapa de Zonas Deforestadas por Tipo de Vegetación")
mapa_vegetacion = mapa_deforestacion(df[df['Tipo_Vegetacion'].notnull()], 'Tipo_Vegetacion', color='red')
st.write(mapa_vegetacion)

# Mapas de las zonas deforestadas por altitud
st.subheader("Mapa de Zonas Deforestadas por Altitud")
mapa_altitud = mapa_deforestacion(df[df['Altitud'].notnull()], 'Altitud', color='blue')
st.write(mapa_altitud)

# Mapas de las zonas deforestadas por precipitación
st.subheader("Mapa de Zonas Deforestadas por Precipitación")
mapa_precipitacion = mapa_deforestacion(df[df['Precipitacion'].notnull()], 'Precipitacion', color='green')
st.write(mapa_precipitacion)

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
        mapa_personalizado = mapa_deforestacion(df_filtrado, 'Latitud', color='orange')
        st.write(mapa_personalizado)
    else:
        st.write("No hay datos que coincidan con los filtros seleccionados.")
