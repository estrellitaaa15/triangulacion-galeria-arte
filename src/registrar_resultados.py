#Importa librerías para exportar tablas CSV, manejar rutas, medir tiempos de CPU y registrar fechas
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

#Calcula el área exacta del polígono original usando la fórmula de determinantes (Shoelace)
def calcularAreaPoligono(coords: list[tuple[float, float]]) -> float:
    n = len(coords)
    suma = 0.0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        suma += (x1 * y2 - x2 * y1)
    return abs(suma) / 2.0

#Suma el área individual de todos los triángulos generados (la mitad del producto cruz de cada triángulo)
def calcularAreaTriangulos(triangulos: list[tuple[Point, Point, Point]]) -> float:
    return sum(abs(Point.crossProduct(p1, p2, p3)) / 2.0 for p1, p2, p3 in triangulos)


def ejecutarYGuardarResultados(
    rutaJson: str = "data/poligonos_benchmark.json",
    rutaCsv: str = "resultados/historial_pruebas_optimo.csv",
    rutaTablaTxt: str = "resultados/tabla_pruebas_optimo.txt",
    repeticiones: int = 5,
    limiteTiempoSeg: float = 5.0,
):
    #Crea la carpeta de resultados si aún no existe en el repositorio
    os.makedirs(os.path.dirname(rutaCsv), exist_ok=True)
    #Si todavía no existe el archivo JSON con polígonos, genera un conjunto base automáticamente para evitar errores
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

    #Ordenar instancias de menor a mayor número de vértices (n)
    instanciasOrdenadas = sorted(dataset.items(), key=lambda item: len(item[1]))

    #Define las columnas para el archivo CSV y el formato alineado de la tabla visual en texto
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

    #Abre el CSV en modo agregar ('a') para conservar el historial de todas las corridas anteriores
    with open(rutaCsv, mode="a", newline="", encoding="utf-8") as archivoCsv:
        escritor = csv.writer(archivoCsv)
        if not archivoCsvExiste:
            escritor.writerow(encabezadosCsv)

        for nombreInstancia, coords in instanciasOrdenadas:
            tiemposSeg = []
            ultimoResultado = None
            excedioLimite = False

            #Ejecuta el algoritmo varias veces con un cronómetro de alta precisión para promediar el tiempo de CPU
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

            #Si alguna instancia tarda más del límite permitido, detiene el experimento y lo registra en la tabla
            if excedioLimite:
                filaTxt = (
                    f"{nombreInstancia:<14} | {n:>4} | {f'> {limiteTiempoSeg:.1f}s':>10} | "
                    f"{'-':>11} | {'-':>11} | {'-':>10} | {'-':>10} | {'-':>9} | {'límite de tiempo':<10}"
                )
                lineasTabla.append(filaTxt)
                break

            #Extrae el total de triángulos, diagonales, cámaras asignadas y el límite máximo de Fisk (n // 3)
            nTriangulos = len(ultimoResultado["triangulos"])
            nDiagonales = nTriangulos - 1
            nCamaras = len(ultimoResultado["camaras"])
            cotaFisk = n // 3

            #Toma el contador exacto si existe en TrianguladorPoligono o estima operaciones base
            trianguladorObj = ultimoResultado["triangulador"]
            operaciones = getattr(trianguladorObj, "operaciones", 0)
            if operaciones == 0:
                #Conteo mínimo estructural: ordenamiento + barrido + pila + árbol dual + BFS
                operaciones = (n * (n.bit_length())) + (3 * n) + nTriangulos
            #Comprueba que la suma de áreas de los triángulos coincida con el área original sin solapamientos
            areaOriginal = calcularAreaPoligono(coords)
            areaTriangulada = calcularAreaTriangulos(ultimoResultado["triangulos"])
            diffArea = abs(areaOriginal - areaTriangulada)

            #Verifica que se cumplan todos los invariantes geométricos y teóricos para marcar la prueba como OK
            esValida = (
                (nTriangulos == n - 2)
                and (nDiagonales == n - 3)
                and (nCamaras <= cotaFisk)
                and (diffArea < 1e-6)
            )
            estadoStr = "OK" if esValida else "ERROR"
            camarasStr = f"{nCamaras}/{cotaFisk}"

            #Escribe la fila de datos en el CSV y da formato visual a la fila de la tabla en texto
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
    #Guarda la tabla formateada en el archivo .txt y la imprime directamente en la terminal
    with open(rutaTablaTxt, mode="a", encoding="utf-8") as archivoTxt:
        archivoTxt.write(contenidoTabla + "\n")

    print("\n" + contenidoTabla)
    print(f"\nTabla visual guardada en: {rutaTablaTxt}")
    print(f"Datos guardados en: {rutaCsv}\n")


if __name__ == "__main__":
    ejecutarYGuardarResultados()