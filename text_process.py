from collections import Counter
import re

def contar_apellidos(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    # Lista de palabras técnicas y comunes en textos científicos que no son apellidos
    palabras_ignoradas = {
        "título", "citado", "por", "año", "volume", "issue", "pages",
        "the", "of", "in", "and", "on", "for", "with", "at", "by", "an",
        "physical", "science", "solid", "state", "nature", "magnetic", "order",
        "review", "physics", "matter", "condensed", "spin", "chemistry",
        "international", "journal", "research", "materials", "investigation",
        "high", "temperature", "superconductor", "study", "system", "effect",
        "conductivity", "field", "superconductivity", "physica", "model",
        "behavior", "structure", "properties", "function", "method", "analysis", "phase", "nuclear", "abstracts"
        "Meeting", "march", "letters", "charge", "Abstracts"
    }
    
    apellidos = []
    for linea in lineas:
        # Buscar palabras en mayúscula que parecen apellidos (mínimo 3 letras)
        palabras = re.findall(r'\b[A-Z][a-z]{2,}\b', linea)
        for palabra in palabras:
            palabra_min = palabra.lower()
            # Ignorar palabras en lista de palabras técnicas
            if palabra_min not in palabras_ignoradas:
                apellidos.append(palabra)
    
    # Contar la frecuencia de cada apellido
    contador_apellidos = Counter(apellidos)
    
    # Obtener el top 10
    top_20 = contador_apellidos.most_common(20)
    
    return top_20

# Ejecutar la función y mostrar los resultados
archivo = 'nombres.txt'  # Nombre de tu archivo
top_10_apellidos = contar_apellidos(archivo)
print("Top 10 apellidos más frecuentes:")
for apellido, frecuencia in top_10_apellidos:
    print(f"{apellido}: {frecuencia} veces")
