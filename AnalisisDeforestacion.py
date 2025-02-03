import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar el archivo CSV desde una URL o desde el sistema local
def cargar_datos():
    opcion = st.selectbox("¿Cómo te gustaría cargar los datos?", ["Subir archivo CSV", "Leer desde URL"])
    
    if opcion == "Subir archivo CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            return df
    
    elif opcion == "Leer desde URL":
        url = st.text_input("Introduce la URL del archivo CSV")
        if url:
            df = pd.read_csv(url)
            return df

    return None

# Función para realizar el análisis de deforestación
def analizar_deforestacion(df):
    st.subheader("Análisis de Deforestación")

    # 1. Superficie total deforestada
    superficie_total = df['Superficie_Deforestada'].sum()
    st.write(f"**Superficie total deforestada:** {superficie_total:.2f} hectáreas")

    # 2. Tasa promedio de deforestación
    tasa_promedio = df['Tasa_Deforestacion'].mean()
    st.write(f"**Tasa promedio de deforestación:** {tasa_promedio:.2f} % anual")

    # 3. Tendencia de la tasa de deforestación a lo largo del tiempo
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df_tendencia = df.groupby(df['Fecha'].dt.year)['Tasa_Deforestacion'].mean().reset_index()

    # Graficar la tendencia
    plt.figure(figsize=(10, 6))
    plt.plot(df_tendencia['Fecha'], df_tendencia['Tasa_Deforestacion'], marker='o', color='b')
    plt.title("Tasa de deforestación a lo largo del tiempo")
    plt.xlabel("Año")
    plt.ylabel("Tasa de deforestación (%)")
    st.pyplot(plt)

# Función principal para la app
def main():
    st.title("Análisis de Deforestación")
    
    # Cargar los datos
    df = cargar_datos()
    
    if df is not None:
        # Mostrar los datos originales
        st.subheader("Vista previa de los datos")
        st.write(df.head())

        # Realizar el análisis de deforestación
        analizar_deforestacion(df)

# Ejecutar la app
if __name__ == "__main__":
    main()
