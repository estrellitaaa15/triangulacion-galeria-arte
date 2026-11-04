# Pruebas de creación de un polígono pequeño (como un cuadrado o hexágono) 
# para saber si el algoritmo de fuerza bruta logra triangularlo sin fallas
from src.fuerza_bruta import brute_force_triangulation, construir_grafo_dual, tres_coloracion, seleccionar_camaras, verificar_colores

def resolver(nombre, vertices):
    print(f"\n=== {nombre} (n = {len(vertices)}) ===")

    triangulos = brute_force_triangulation(vertices)
    print(f"Triángulos: {len(triangulos)} (esperados: {len(vertices) - 2})")

    adyacencia = construir_grafo_dual(triangulos)
    aristas_dual = sum(len(v) for v in adyacencia.values()) // 2
    print(f"Árbol dual: {len(triangulos)} nodos, {aristas_dual} aristas "
          f"(esperadas: {len(vertices) - 3})")
    for i, vecinos in adyacencia.items():
        print(f"  T{i + 1} -> {['T' + str(j + 1) for j in vecinos]}")

    colores = tres_coloracion(triangulos, adyacencia)
    camaras, grupos = seleccionar_camaras(colores)
    for c in (0, 1, 2):
        print(f"Color {c}: {sorted(grupos[c], key=lambda p: p.id)}")

    print(f"Cámaras ({len(camaras)}, límite {len(vertices) // 3}): {camaras}")

    ok_colores, ok_cobertura, ok_limite = verificar(
        triangulos, colores, camaras, len(vertices))
    print(f"Cada triángulo con 3 colores distintos: {ok_colores}")
    print(f"Cada triángulo tiene una cámara:        {ok_cobertura}")
    print(f"Cámaras <= floor(n/3):                  {ok_limite}")


if __name__ == "__main__": 
    L = [Point(0, 0, 0), Point(4, 0, 1), Point(4, 2, 2),
         Point(2, 2, 3), Point(2, 5, 4), Point(0, 5, 5)]
    resolver("Polígono en L", L)

    P8 = [Point(0, 0, 0), Point(3, 0, 1), Point(3, 2, 2), Point(6, 2, 3),
          Point(6, 5, 4), Point(4, 7, 5), Point(2, 5, 6), Point(0, 4, 7)]
    resolver("Polígono de 8 vértices", P8)