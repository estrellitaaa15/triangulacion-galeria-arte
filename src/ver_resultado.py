from src.algoritmo_optimo import triangularPoligono, Point
from src.generador_poligonos import generarPoligonoEstrella


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


# 1. Prueba con el polígono en L de 6 vértices (ejemplo de la Fase 1)
poligonoL = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)]
resL = triangularPoligono(poligonoL)

print("=== RESULTADO POLÍGONO EN L (n=6) ===")
print("Diagonales trazadas:", resL["diagonales"])
print("Triángulos generados (n - 2 = 4):")
for i, t in enumerate(resL["triangulos"], 1):
    print(f"  T{i}: {t}")
print("Color asignado a cada vértice:", resL["diccPoint"])
print("Cámaras óptimas (<= 2):", resL["camaras"])
print(f"Área original: {calcularAreaPoligono(poligonoL)} | Suma áreas triángulos: {calcularAreaTriangulos(resL['triangulos'])}")

# 2. Verificación matemática en un polígono de 150 vértices
estrella150 = generarPoligonoEstrella(n=150, seed=42)
res150 = triangularPoligono(estrella150)
areaOrig = calcularAreaPoligono(estrella150)
areaTri = calcularAreaTriangulos(res150["triangulos"])

print("\n=== VERIFICACIÓN POLÍGONO GRANDE (n=150) ===")
print(f"Triángulos: {len(res150['triangulos'])} (esperados: 148)")
print(f"Cámaras: {len(res150['camaras'])} (máximo permitido: {150 // 3})")
print(f"Área original: {areaOrig:.4f} | Suma triángulos: {areaTri:.4f} | Diferencia: {abs(areaOrig - areaTri):.2e}")