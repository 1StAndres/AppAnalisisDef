import streamlit as st
import pandas as pd

# Función para cargar el archivo CSV desde una URL o desde el sistema local
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

# Función para rellenar los valores faltantes mediante interpolación
def rellenar_valores_faltantes(df):
    st.subheader("Rellenar valores faltantes")
    
    # Opción para seleccionar el tipo de interpolación
    metodo = st.selectbox("Elige el método de interpolación", ["lineal", "polinómica", "spline"])

    # Interpolación lineal
    if metodo == "lineal":
        df_interpolado = df.interpolate(method="linear", axis=0)
    
    # Interpolación polinómica (grado 2 como ejemplo)
    elif metodo == "polinómica":
        df_interpolado = df.interpolate(method="polynomial", order=2, axis=0)
    
    # Interpolación spline
    elif metodo == "spline":
        df_interpolado = df.interpolate(method="spline", order=3, axis=0)

    return df_interpolado

# Función principal para la app
def main():
    st.title("Análisis de Deforestación")
    
    # Cargar los datos
    df = cargar_datos()
    
    if df is not None:
        # Mostrar los datos originales
        st.subheader("Vista previa de los datos originales")
        st.write(df.head())

        # Rellenar los valores faltantes con interpolación
        df_interpolado = rellenar_valores_faltantes(df)
        
        # Mostrar los datos después de la interpolación
        st.subheader("Vista previa de los datos después de interpolación")
        st.write(df_interpolado.head())

# Ejecutar la app
if __name__ == "__main__":
    main()

