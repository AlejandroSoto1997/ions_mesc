import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
archivo_csv = 'names.csv'  # Cambia esta ruta al archivo CSV correcto
df = pd.read_csv(archivo_csv, header=None, names=["TÍTULO", "CITADO POR", "AÑO"])

# Listas para cada columna del nuevo DataFrame
titulos = []
citados = []
años = []
autores = []
revistas = []

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

# Extraer el primer y último autor de la lista de autores
nuevo_df['MAIN AUTHOR'] = nuevo_df['AUTORES'].apply(lambda x: x.split(',')[0].strip())
nuevo_df['LAST AUTHOR'] = nuevo_df['AUTORES'].apply(lambda x: x.split(',')[-1].strip())

# Filtrar el DataFrame para incluir solo las filas donde el main author es "C Berthier"
filtered_df_main_author = nuevo_df[nuevo_df['MAIN AUTHOR'] == 'C Berthier'].reset_index(drop=True)

# Filtrar el DataFrame para incluir solo las filas donde el last author es "C Berthier"
filtered_df_last_author = nuevo_df[nuevo_df['LAST AUTHOR'] == 'C Berthier'].reset_index(drop=True)

# Pasos adicionales para las visualizaciones
# Step 1: Aggregate citations by year for the original DataFrame
citations_per_year_total = nuevo_df.groupby('AÑO')['CITADO POR'].sum()

# Step 2: Aggregate citations by year for publications with "C Berthier" as the last author
citations_per_year_berthier_last = filtered_df_last_author.groupby('AÑO')['CITADO POR'].sum()

# Step 3: Plotting
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot citations per year for the original DataFrame and last author overlay in the first subplot
axes[0].plot(citations_per_year_total.index, citations_per_year_total.values, marker='o', color='b', label="All Authors")
axes[0].plot(citations_per_year_berthier_last.index, citations_per_year_berthier_last.values, marker='o', color='r', linestyle='--', label="C Berthier (Last Author)")
axes[0].set_title("Citations Per Year - All Publications (with C Berthier as Last Author)")
axes[0].set_ylabel("Citations")
axes[0].legend()

# Plot citations per year for the filtered DataFrame ("C Berthier" as main author) in the second subplot
citations_per_year_berthier_main = filtered_df_main_author.groupby('AÑO')['CITADO POR'].sum()
axes[1].plot(citations_per_year_berthier_main.index, citations_per_year_berthier_main.values, marker='o', color='g', label="C Berthier (Main Author)")
axes[1].plot(citations_per_year_berthier_last.index, citations_per_year_berthier_last.values, marker='o', color='r', linestyle='--', label="C Berthier (Last Author)")
axes[1].set_title("Citations Per Year - Publications by C Berthier (Main Author)")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Citations")
axes[1].legend()

# Adjust layout for clarity
plt.tight_layout()
plt.show()

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Filter DataFrame for "C Berthier" as Main Author
berthier_main_df = nuevo_df[nuevo_df['MAIN AUTHOR'] == 'C Berthier'].copy()

# Use TF-IDF to extract keywords from the titles
def extract_keywords_tfidf(titles):
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_features=3, stop_words='english')  # max_features controls number of keywords per title
    X = vectorizer.fit_transform(titles)
    
    # Get keywords per title based on highest TF-IDF scores
    keywords_list = []
    for row in X:
        indices = row.nonzero()[1]
        keywords = [vectorizer.get_feature_names_out()[i] for i in indices]
        keywords_list.append(', '.join(keywords))
    return keywords_list

# Apply the function to extract keywords
berthier_main_df['KEYWORDS'] = extract_keywords_tfidf(berthier_main_df['TÍTULO'])
berthier_main_df_sort = berthier_main_df.sort_values(by='AÑO', ascending=True).reset_index(drop=True)



# Display DataFrame with the new keywords column
print(berthier_main_df[['TÍTULO', 'KEYWORDS']])


