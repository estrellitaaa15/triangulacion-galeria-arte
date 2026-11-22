import csv
import os
import time
from datetime import datetime
from src.algoritmo_optimo import triangularPoligono, Point
from src.generador_poligonos import (
    cargarDatasetJson,
    guardarDatasetJson,
    generarPoligonoEstrella,
    generarPoligonoPeine,
)


def calcularAreaPoligono(coords: list[tuple[float, float]]) -> float:
    n = len(coords)
    suma = 0.0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        suma += (x1 * y2 - x2 * y1)
    return abs(suma) / 2.0


def calcularAreaTriangulos(triangulos: list[tuple[Point, Point, Point]]) -> float:
    return sum(abs(Point.crossProduct(p1, p2, p3)) / 2.0 for p1, p2, p3 in triangulos)


def ejecutarYGuardarResultados(
    rutaJson: str = "data/poligonos_benchmark.json",
    rutaCsv: str = "resultados/historial_pruebas_optimo.csv",
    repeticiones: int = 5,
):
    """
    Ejecuta el algoritmo óptimo sobre cada polígono del JSON, promedia el tiempo
    de CPU en milisegundos y guarda todas las métricas en un archivo CSV.
    """
    os.makedirs(os.path.dirname(rutaCsv), exist_ok=True)
    if not os.path.exists(rutaJson):
        os.makedirs(os.path.dirname(rutaJson), exist_ok=True)
        datasetInicial = {
            "L_6": [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)],
            "estrella_20": generarPoligonoEstrella(n=20, seed=10),
            "peine_24": generarPoligonoPeine(kDientes=7),
            "peine_120": generarPoligonoPeine(kDientes=39),
            "estrella_250": generarPoligonoEstrella(n=250, seed=42),
        }
        guardarDatasetJson(rutaJson, datasetInicial)
        print(f"Dataset base creado automáticamente en: {rutaJson}")

    dataset = cargarDatasetJson(rutaJson)
    dataset = cargarDatasetJson(rutaJson)

    encabezados = [
        "fecha_hora",
        "instancia",
        "n_vertices",
        "tiempo_promedio_ms",
        "tiempo_min_ms",
        "triangulos_obtenidos",
        "triangulos_esperados",
        "diagonales_obtenidas",
        "camaras_asignadas",
        "cota_max_fisk",
        "diferencia_area",
        "solucion_valida",
    ]

    archivoExiste = os.path.exists(rutaCsv)
    marcaTiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(rutaCsv, mode="a", newline="", encoding="utf-8") as archivoCsv:
        escritor = csv.writer(archivoCsv)
        if not archivoExiste:
            escritor.writerow(encabezados)

        for nombreInstancia, coords in dataset.items():
            tiemposMs = []
            ultimoResultado = None

            # Ejecutar varias veces para obtener un tiempo de CPU estable
            for _ in range(repeticiones):
                inicio = time.perf_counter()
                ultimoResultado = triangularPoligono(coords)
                fin = time.perf_counter()
                tiemposMs.append((fin - inicio) * 1000.0)

            n = ultimoResultado["nVertices"]
            nTriangulos = len(ultimoResultado["triangulos"])
            nDiagonales = nTriangulos - 1
            nCamaras = len(ultimoResultado["camaras"])
            cotaFisk = n // 3

            areaOriginal = calcularAreaPoligono(coords)
            areaTriangulada = calcularAreaTriangulos(ultimoResultado["triangulos"])
            diffArea = abs(areaOriginal - areaTriangulada)

            esValida = (
                (nTriangulos == n - 2)
                and (nDiagonales == n - 3)
                and (nCamaras <= cotaFisk)
                and (diffArea < 1e-6)
            )

            tiempoPromedio = sum(tiemposMs) / len(tiemposMs)
            tiempoMinimo = min(tiemposMs)

            escritor.writerow([
                marcaTiempo,
                nombreInstancia,
                n,
                round(tiempoPromedio, 4),
                round(tiempoMinimo, 4),
                nTriangulos,
                n - 2,
                nDiagonales,
                nCamaras,
                cotaFisk,
                f"{diffArea:.2e}",
                esValida,
            ])

            print(
                f"[OK] {nombreInstancia:<14} | n={n:<4} | "
                f"Tiempo: {tiempoPromedio:>8.3f} ms | "
                f"Triángulos: {nTriangulos}/{n-2} | "
                f"Cámaras: {nCamaras}/{cotaFisk}"
            )

    print(f"\nResultados guardados en: {rutaCsv}")


if __name__ == "__main__":
    ejecutarYGuardarResultados()