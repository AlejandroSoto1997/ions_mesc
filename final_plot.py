import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import scienceplots
plt.style.use(['science', 'no-latex', 'bright'])

# Cargar el archivo CSV
archivo_csv = 'names.csv'  # Cambia esta ruta al archivo CSV correcto
df = pd.read_csv(archivo_csv, header=None, names=["TÍTULO", "CITADO POR", "AÑO"])

# Listas para cada columna del nuevo DataFrame
titulos = []
citados = []
años = []
autores = []
revistas = []

font_sizes = {
    'title': 16,
    'xlabel': 14,
    'ylabel': 14,
    'legend': 12,
    'tick_labels': 12
}


# Procesar los datos en bloques de 3 filas (título, autores, revista)
for i in range(0, len(df), 3):
    # Extraer título, citado por y año
    titulo = df.iloc[i]["TÍTULO"]
    citado_por = df.iloc[i]["CITADO POR"]
    año = df.iloc[i]["AÑO"]
    
    # Extraer autores y revista de las filas siguientes
    autor = df.iloc[i + 1]["TÍTULO"] if i + 1 < len(df) else ""
    revista = df.iloc[i + 2]["TÍTULO"] if i + 2 < len(df) else ""
    
    # Agregar a las listas correspondientes
    titulos.append(titulo)
    citados.append(citado_por)
    años.append(año)
    autores.append(autor)
    revistas.append(revista)

# Crear el nuevo DataFrame
nuevo_df = pd.DataFrame({
    'TÍTULO': titulos,
    'CITADO POR': citados,
    'AÑO': años,
    'AUTORES': autores,
    'REVISTA': revistas
})

# Limpiar los valores de "CITADO POR" para convertirlos a números y asegurarse de que sean positivos
nuevo_df['CITADO POR'] = pd.to_numeric(nuevo_df['CITADO POR'], errors='coerce').fillna(0)
nuevo_df['CITADO POR'] = nuevo_df['CITADO POR'].clip(lower=0)  # Convertir a 0 cualquier valor negativo

# Extraer el primer autor de la lista de autores
nuevo_df['MAIN AUTHOR'] = nuevo_df['AUTORES'].apply(lambda x: x.split(',')[0].strip())

# Filtrar el DataFrame para incluir solo las filas donde el main author es "C Berthier"
filtered_df_main_author = nuevo_df[nuevo_df['MAIN AUTHOR'] == 'C Berthier'].reset_index(drop=True)

# Agregar citas por año
citations_per_year_total = nuevo_df.groupby('AÑO')['CITADO POR'].sum()
citations_per_year_main = filtered_df_main_author.groupby('AÑO')['CITADO POR'].sum()

# Interpolación para suavizar las curvas
def smooth_curve(x, y, points=300):
    x_smooth = np.linspace(x.min(), x.max(), points)
    y_smooth = make_interp_spline(x, y, k=3)(x_smooth)  # Cubic spline
    y_smooth = np.maximum(y_smooth, 0)  # Reemplazar valores negativos por 0
    return x_smooth, y_smooth

# Datos suavizados
x_total, y_total = smooth_curve(citations_per_year_total.index, citations_per_year_total.values)
x_main, y_main = smooth_curve(citations_per_year_main.index, citations_per_year_main.values)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import scienceplots

# Estilo de la gráfica
plt.style.use(['science', 'no-latex', 'bright'])

# Diccionario de tamaños de fuente
font_sizes = {
    'title': 16,
    'xlabel': 14,
    'ylabel': 14,
    'legend': 12,
    'tick_labels': 12,
    'text_bands': 12  # Tamaño del texto dentro de las bandas de colores
}

# Crear la gráfica
plt.figure(figsize=(10, 3.5))

# Rellenar el área bajo la curva de publicaciones totales
plt.fill_between(x_total, y_total, where=(y_total > 0), color='black', alpha=0.09, label="All papers")

# Plot de la curva suavizada para C Berthier
plt.plot(x_main, y_main, label="Main authorship", color='black', alpha=0.8)

# Sombrar el fondo por rangos de años
plt.axvspan(1972, 1975, color='green', alpha=0.1, ymin=0, ymax=1)
plt.axvspan(1975, 1977, color='yellow', alpha=0.1, ymin=0, ymax=1)
plt.axvspan(1977, 1978, color='purple', alpha=0.1, ymin=0, ymax=1)
plt.axvspan(1978, 1983, color='#9e0142', alpha=0.15, ymin=0, ymax=1)
plt.axvspan(1983, 1990, color='#3288bd', alpha=0.2, ymin=0, ymax=1)
plt.axvspan(1990, 1997, color='gray', alpha=0.2, ymin=0, ymax=1)
plt.axvspan(2000, 2017, color='pink', alpha=0.3, ymin=0, ymax=1)

# Añadir texto a cada banda de color
plt.text(1973.5, 1000, "Alloys", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(1976, 1000, "TMD", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(1977.5, 1000, "Lamellar", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(1980.5, 1000, r"PX$_{3}$", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(1986.5, 1000, "Lamellar", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(1993.5, 1000, "Ceramic", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.text(2002.5, 1000, "Review", color="black", ha='center', fontsize=font_sizes['text_bands'], rotation=90)
plt.axvline(x=1982.6, color='red', linestyle='--', linewidth=1.5, alpha=0.8,label="Paper of "+r"$P(EO)_n M^+ X^-$")

# Etiquetas de los ejes
plt.xlabel("Year", fontsize=font_sizes['xlabel'])
plt.ylabel("Number of cites", fontsize=font_sizes['ylabel'])

# Crear leyenda con fondo blanco
legend = plt.legend(
    fontsize=font_sizes['legend'],
    frameon=True,  # Habilitar el cuadro alrededor de la leyenda
    facecolor='white',  # Color de fondo de la leyenda
    edgecolor='black'  # Borde de la leyenda
)

# Límites de los ejes
plt.xlim(1970, 2022)
plt.ylim(bottom=0)  # Fijar el límite inferior del eje y en 0

# Ajustar los ticks en el eje X
plt.xticks(ticks=np.arange(1970, 2025, 5), fontsize=font_sizes['tick_labels'])  # Cada 5 años entre 1970 y 2025

# Ajustar los ticks en el eje Y
plt.yticks(ticks=np.arange(50, 1601, 250), fontsize=font_sizes['tick_labels'])  # Cada 250 entre 0 y 1500



plt.tight_layout()
plt.savefig('timeline.png', dpi=600)
# Mostrar la gráfica
plt.show()
