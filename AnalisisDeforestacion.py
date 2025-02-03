import geopandas as gpd
import matplotlib.pyplot as plt

# URL del CSV
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"

# Ruta del mapa del mundo
ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"

# Cargar el mapa del mundo
mundo_dataframe = gpd.read_file(ruta_0)

# Cargar datos de deforestación (reutilizar la función load_data)
df = load_data(data_url)

if df is None:
    print("Error al cargar los datos. Saliendo del programa.")
    exit()

# Check for required columns *after* loading the data
required_columns = ["Latitud", "Longitud"]
if all(col in df.columns for col in required_columns):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["Longitud"], df["Latitud"]))

    # Crear el mapa base con el mapa del mundo
    fig, ax = plt.subplots(figsize=(10, 10))
    mundo_dataframe.plot(ax=ax, color='lightgray', edgecolor='black')

    # Superponer los puntos de deforestación
    gdf.plot(ax=ax, marker='o', color='red', markersize=10)

    # Ajustar la vista del mapa (opcional, si quieres enfocar una región específica)
    # ax.set_xlim(-60, -30)  # Ejemplo: enfocar en Sudamérica
    # ax.set_ylim(-30, 10)

    # Guardar el mapa en un archivo
    plt.savefig('mapa_deforestacion_geopandas.png')
    print("Mapa generado exitosamente en mapa_deforestacion_geopandas.png")

else:
    print(f"Las columnas {required_columns} no se encuentran en el DataFrame. "
          f"Verifica los nombres de las columnas.")
    print(df.columns.tolist())
