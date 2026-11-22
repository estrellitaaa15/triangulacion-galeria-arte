#Librerias: 'json' para guardar/leer archivos, 'math' para trigonometría (cos, sin, pi)
#y 'random' para generar ángulos y radios aleatorios controlados.
import json
import math
import random


def generarPoligonoEstrella(n: int, radioMin: float = 20.0, radioMax: float = 100.0, seed: int = 42) -> list[tuple[float, float]]:
    """
    Genera un polígono simple garantizado de n vértices en sentido antihorario
    variando los radios para producir múltiples vértices SPLIT y MERGE.
    """
    #Crea n ángulos entre 0 y 2*pi y los ordena, al ir en orden angular creciente alrededor del origen, es imposible que se crucen las aristas
    rng = random.Random(seed)
    angulos = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
    puntos = []

    #Asigna un radio aleatorio a cada ángulo (alternando picos
    #y valles reflejos) y calcula sus coordenadas (x, y) con x = r*cos(theta) y y = r*sin(theta).
    for theta in angulos:
        r = rng.uniform(radioMin, radioMax)
        x = round(r * math.cos(theta), 4)
        y = round(r * math.sin(theta), 4)
        puntos.append((x, y))
    return puntos


def generarPoligonoPeine(kDientes: int) -> list[tuple[float, float]]:
    """
    Genera el Polígono Peine de Chvátal con n = 3 * kDientes vértices.
    Es el peor caso del Problema de la Galería de Arte (requiere exactamente n/3 cámaras).
    """
    puntos = [(0.0, 0.0), (kDientes * 4.0, 0.0), (kDientes * 4.0, 2.0)]
    #Construcción de dientes de derecha a izquierda, recorre en reversa para cerrar el contorno sin cruzar paredes; cada diente agrega base derecha, punta alta (y=10) y base izquierda
    for i in range(kDientes - 1, -1, -1):
        xDer = i * 4.0 + 3.0
        xPunta = i * 4.0 + 2.0
        xIzq = i * 4.0 + 1.0
        puntos.append((xDer, 2.0))
        puntos.append((xPunta, 10.0))
        puntos.append((xIzq, 2.0))
    return puntos

#Serializa el diccionario de polígonos a texto estructurado y legible
def guardarDatasetJson(ruta: str, dataset: dict):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(dataset, archivo, indent=2)

#Lee un archivo .json existente y lo transforma de regreso en un diccionario de Python listo para usarse en las pruebas y gráficas.
def cargarDatasetJson(ruta: str) -> dict:
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)