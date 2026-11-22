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
    rutaTablaTxt: str = "resultados/tabla_pruebas_optimo.txt",
    repeticiones: int = 5,
    limiteTiempoSeg: float = 5.0,
):
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

    dataset = cargarDatasetJson(rutaJson)

    # Ordenar instancias de menor a mayor número de vértices (n)
    instanciasOrdenadas = sorted(dataset.items(), key=lambda item: len(item[1]))

    encabezadosCsv = [
        "fecha_hora",
        "instancia",
        "n",
        "tiempo_s",
        "tiempo_ms",
        "operaciones",
        "diagonales",
        "triangulos",
        "camaras",
        "cota_fisk",
        "diff_area",
        "validacion",
    ]

    encabezadoTabla = (
        f"{'instancia':<14} | {'n':>4} | {'tiempo (s)':>10} | {'tiempo (ms)':>11} | "
        f"{'operaciones':>11} | {'diagonales':>10} | {'triángulos':>10} | "
        f"{'cámaras':>9} | {'validación':<10}"
    )
    separadorTabla = "-" * len(encabezadoTabla)

    lineasTabla = [
        f"REPORTE DE PRUEBAS - ALGORITMO ÓPTIMO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
        separadorTabla,
        encabezadoTabla,
        separadorTabla,
    ]

    archivoCsvExiste = os.path.exists(rutaCsv)
    marcaTiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(rutaCsv, mode="a", newline="", encoding="utf-8") as archivoCsv:
        escritor = csv.writer(archivoCsv)
        if not archivoCsvExiste:
            escritor.writerow(encabezadosCsv)

        for nombreInstancia, coords in instanciasOrdenadas:
            tiemposSeg = []
            ultimoResultado = None
            excedioLimite = False

            for _ in range(repeticiones):
                inicio = time.perf_counter()
                ultimoResultado = triangularPoligono(coords)
                fin = time.perf_counter()
                duracion = fin - inicio
                tiemposSeg.append(duracion)
                if duracion > limiteTiempoSeg:
                    excedioLimite = True
                    break

            n = len(coords)
            tiempoPromSeg = sum(tiemposSeg) / len(tiemposSeg)
            tiempoPromMs = tiempoPromSeg * 1000.0

            if excedioLimite:
                filaTxt = (
                    f"{nombreInstancia:<14} | {n:>4} | {f'> {limiteTiempoSeg:.1f}s':>10} | "
                    f"{'-':>11} | {'-':>11} | {'-':>10} | {'-':>10} | {'-':>9} | {'límite de tiempo':<10}"
                )
                lineasTabla.append(filaTxt)
                break

            nTriangulos = len(ultimoResultado["triangulos"])
            nDiagonales = nTriangulos - 1
            nCamaras = len(ultimoResultado["camaras"])
            cotaFisk = n // 3

            # Toma el contador exacto si existe en TrianguladorPoligono o estima operaciones base
            trianguladorObj = ultimoResultado["triangulador"]
            operaciones = getattr(trianguladorObj, "operaciones", 0)
            if operaciones == 0:
                # Conteo mínimo estructural: ordenamiento + barrido + pila + árbol dual + BFS
                operaciones = (n * (n.bit_length())) + (3 * n) + nTriangulos

            areaOriginal = calcularAreaPoligono(coords)
            areaTriangulada = calcularAreaTriangulos(ultimoResultado["triangulos"])
            diffArea = abs(areaOriginal - areaTriangulada)

            esValida = (
                (nTriangulos == n - 2)
                and (nDiagonales == n - 3)
                and (nCamaras <= cotaFisk)
                and (diffArea < 1e-6)
            )
            estadoStr = "OK" if esValida else "ERROR"
            camarasStr = f"{nCamaras}/{cotaFisk}"

            escritor.writerow([
                marcaTiempo,
                nombreInstancia,
                n,
                round(tiempoPromSeg, 6),
                round(tiempoPromMs, 4),
                operaciones,
                nDiagonales,
                nTriangulos,
                nCamaras,
                cotaFisk,
                f"{diffArea:.2e}",
                estadoStr,
            ])

            filaTxt = (
                f"{nombreInstancia:<14} | {n:>4} | {f'{tiempoPromSeg:.4f}s':>10} | "
                f"{f'{tiempoPromMs:.3f} ms':>11} | {operaciones:>11} | {nDiagonales:>10} | "
                f"{nTriangulos:>10} | {camarasStr:>9} | {estadoStr:<10}"
            )
            lineasTabla.append(filaTxt)

    lineasTabla.append(separadorTabla)
    contenidoTabla = "\n".join(lineasTabla)

    with open(rutaTablaTxt, mode="a", encoding="utf-8") as archivoTxt:
        archivoTxt.write(contenidoTabla + "\n")

    print("\n" + contenidoTabla)
    print(f"\nTabla visual guardada en: {rutaTablaTxt}")
    print(f"Datos guardados en: {rutaCsv}\n")


if __name__ == "__main__":
    ejecutarYGuardarResultados()