import os
from src.generador_poligonos import (
    generarPoligonoEstrella,
    generarPoligonoPeine,
    guardarDatasetJson,
    cargarDatasetJson,
)

RUTA_DATASET = "data/poligonos_benchmark.json"


def agregarPoligonoAJson(nombrePrueba: str, coordenadas: list[tuple[float, float]], ruta: str = RUTA_DATASET):
    """Carga el JSON existente (si ya existe), agrega un polígono nuevo sin borrar los anteriores y guarda."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    if os.path.exists(ruta):
        dataset = cargarDatasetJson(ruta)
    else:
        dataset = {}

    dataset[nombrePrueba] = coordenadas
    guardarDatasetJson(ruta, dataset)
    print(f"Guardado '{nombrePrueba}' ({len(coordenadas)} vértices) en {ruta}. Total de pruebas: {len(dataset)}")


if __name__ == "__main__":
    # 1. Casos base del protocolo (pequeños, medianos y >100 vértices)
    agregarPoligonoAJson("L_6", [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)])
    agregarPoligonoAJson("estrella_20", generarPoligonoEstrella(n=20, seed=10))
    agregarPoligonoAJson("peine_24", generarPoligonoPeine(kDientes=7))
    agregarPoligonoAJson("peine_120", generarPoligonoPeine(kDientes=39))
    agregarPoligonoAJson("estrella_250", generarPoligonoEstrella(n=250, seed=42))
