import streamlit as st
import pandas as pd

# Función para cargar el archivo CSV desde una URL o desde el sistema local
@st.cache
def cargar_datos():
    # Opción para elegir la fuente de los datos
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

# Función principal para la app
def main():
    st.title("Análisis de Deforestación")
    
    # Cargar los datos
    df = cargar_datos()
    
    if df is not None:
        st.subheader("Vista previa de los datos")
        st.write(df.head())  # Mostrar las primeras filas para verificar los datos

# Ejecutar la app
if __name__ == "__main__":
    main()
