#Importa 'os' para manejar carpetas, las funciones del generador
#y define la ubicación estándar donde se guardarán todos los polígonos de prueba.
import os
from src.generador_poligonos import (
    generarPoligonoEstrella,
    generarPoligonoPeine,
    guardarDatasetJson,
    cargarDatasetJson,
)

RUTA_DATASET = "data/poligonos_benchmark.json"


def agregarPoligonoAJson(nombrePrueba: str, coordenadas: list[tuple[float, float]], ruta: str = RUTA_DATASET):
    #Carga el JSON existente (si ya existe), agrega un polígono nuevo sin borrar los anteriores y guarda
    #Crea la carpeta 'data/' automáticamente si todavía no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    #Lectura sin sobrescribir, si el archivo JSON ya existe, recupera las pruebas guardadas; de lo contrario, inicia un diccionario vacío para empezar desde cero.
    if os.path.exists(ruta):
        dataset = cargarDatasetJson(ruta)
    else:
        dataset = {}

    dataset[nombrePrueba] = coordenadas
    guardarDatasetJson(ruta, dataset)
    print(f"Guardado '{nombrePrueba}' ({len(coordenadas)} vértices) en {ruta}. Total de pruebas: {len(dataset)}")

#Poligonos a triangular, generados con parametros manuales junto al método generarPoligonoEstrella y generarPoligonoPeine
if __name__ == "__main__":
    agregarPoligonoAJson("L_6", [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)])
    agregarPoligonoAJson("estrella_20", generarPoligonoEstrella(n=20, seed=10))
    agregarPoligonoAJson("peine_24", generarPoligonoPeine(kDientes=7))
    #Polígonos tipo Peine, es el peor caso teórico de galería de arte; total de vértices = 3 + 3 * kDientes
    agregarPoligonoAJson("peine_120", generarPoligonoPeine(kDientes=39))
    agregarPoligonoAJson("estrella_250", generarPoligonoEstrella(n=250, seed=42))