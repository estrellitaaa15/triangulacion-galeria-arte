# Evalúa TODAS las posibles combinaciones de diagonales 
# para encontrar una válida.

from collections import deque
from itertools import combinations
from src.dcel import Point, cross_product, is_point_in_triangle
import math


def is_ear(p_prev, p_curr, p_next, polygon):

    # Un vérrice es oreja si es convexo y no contiene ningún otro vértice del polígono en su interior.
    if cross_product(p_prev, p_curr, p_next) <= 0:
        return False

    for pt in polygon:
        if pt in (p_prev, p_curr, p_next):
            continue
        if is_point_in_triangle(pt, p_prev, p_curr, p_next):
            return False
    return True

def brute_force_triangulation(vertices):
    # Recibe los vértices en orden antihorario y retorna una lista de triángulos (cada uno representado por una tupla de tres vértices)
    polygon = vertices[:]
    triangles = []

    while len(polygon) > 3:
        n = len(polygon)
        ear_found = False
        
        for i in range(n):
            p_prev = polygon[i - 1]
            p_curr = polygon[i]
            p_next = polygon[(i + 1) % n]

            if is_ear(p_prev, p_curr, p_next, polygon):

                triangles.append((p_prev, p_curr, p_next))
                polygon.pop(i) # se corta la oreja
                ear_found = True
                break
        
        if not ear_found:
            raise ValueError("Error: Polígono no simple o degenerado.")

    triangles.append((polygon[0], polygon[1], polygon[2]))
    return triangles


def construir_grafo_dual(triangulos):
    #Cada triángulo es un nodo, dos triángulos son adyacentes si comparten una arista. Retorna un diccionario de adyacencia.
    adyacencia = {i: [] for i in range(len(triangulos))}
    aristas = {}  # arista --> lista de triángulos que la contienen

    for i, (a, b, c) in enumerate(triangulos):
        for u, v in ((a, b), (b, c), (c, a)):
            clave = frozenset((u.id, v.id))
            aristas.setdefault(clave, []).append(i)

    for lista in aristas.values():
        if len(lista) == 2:    #arista compartida = diagonal
            i, j = lista
            adyacencia[i].append(j)
            adyacencia[j].append(i)

    return adyacencia
    
def tres_coloracion(triangulos, adyacencia):
    # Colorea los vértices con 3 colores (0, 1, 2) recorriendo el árbol dual con BFS.
    colores = {}
    # El primer triángulo se colorea directamente
    a, b, c = triangulos[0]
    colores[a], colores[b], colores[c] = 0, 1, 2    
    
    visitados = {0}
    fila = deque([0])

    while fila:
        actual = fila.popleft()
        for vecino in adyacencia[actual]:
            if vecino in visitados:
                continue
            visitados.add(vecino)

            #Colores que ya tiene este triágulo vecino, para no repetirlos
            colores_usados = {colores[p] for p in triangulos[vecino] if p in colores}

            #El vértice sin color recibe el color que falta
            for p in triangulos[vecino]:
                if p not in colores:
                    colores[p] = ({0,1,2} - colores_usados).pop()
            fila.append(vecino)

    return colores


def seleccionar_camaras(colores):
    # Elige el color con menos vértices ahí van las cámaras
    grupos = {0: [], 1: [], 2: []}
    for punto, color in colores.items():
        grupos[color].append(punto)

    mejor = min(grupos, key=lambda c: len(grupos[c]))
    return sorted(grupos[mejor], key=lambda p: p.id), grupos


def verificar(triangulos, colores, camaras, n):
    # Revisa que todo cumple con las condiciones del problema: cada triángulo tiene 3 colores distintos, cada triángulo tiene al menos una cámara y el número de cámaras es <= floor(n/3)
    tres_colores = all(len({colores[p] for p in t}) == 3 for t in triangulos)
    cubiertos = all(any(p in camaras for p in t) for t in triangulos)
    limite = len(camaras) <= n // 3
    return tres_colores, cubiertos, limite


def punto_en_segmento(punto, a, b, epsilon=1e-9):
    orientacion = cross_product(a, b, punto)
    dentro_ejes = (
        min(a.x, b.x) - epsilon <= punto.x <= max(a.x, b.x) + epsilon
        and min(a.y, b.y) - epsilon <= punto.y <= max(a.y, b.y) + epsilon
    )
    return abs(orientacion) <= epsilon and dentro_ejes


def punto_en_poligono(punto, vertices):
    dentro = False
    for i, a in enumerate(vertices):
        b = vertices[(i + 1) % len(vertices)]
        if punto_en_segmento(punto, a, b):
            return True
        if (a.y > punto.y) != (b.y > punto.y):
            x_cruce = a.x + (punto.y - a.y) * (b.x - a.x) / (b.y - a.y)
            if punto.x < x_cruce:
                dentro = not dentro
    return dentro


def segmento_visible(desde, hasta, vertices):
    """Comprueba que el segmento se mantenga dentro del polígono."""
    # Muestreo denso: cubre vértices y también el interior de los segmentos.
    for paso in range(101):
        t = paso / 100
        punto = Point(
            desde.x + t * (hasta.x - desde.x),
            desde.y + t * (hasta.y - desde.y),
            -1,
        )
        if not punto_en_poligono(punto, vertices):
            return False
    return True


def vertices_cubiertos(camara, vertices, triangulos):
    """Retorna los vértices visibles desde una cámara."""
    return [
        vertice for vertice in vertices
        if segmento_visible(camara, vertice, vertices)
    ]


def resolver_minimo_por_fuerza_bruta(nombre, vertices):
    """Busca la menor cantidad de cámaras probando todos los subconjuntos."""
    print(f"\n=== {nombre} (n = {len(vertices)}) ===")

    triangulos = brute_force_triangulation(vertices)
    print(f"Triangulación inicial: {len(triangulos)} triángulos")
    for indice, triangulo in enumerate(triangulos, 1):
        print(f"  T{indice}: {[p.id for p in triangulo]}")

    mejor = None
    for cantidad in range(1, len(vertices) + 1):
        candidatas = list(combinations(vertices, cantidad))
        print(f"Probando {len(candidatas)} combinación(es) con {cantidad} cámara(s)")
        for camaras in candidatas:
            ids = [p.id for p in camaras]
            cubiertos = set()
            for camara in camaras:
                for vertice in vertices_cubiertos(camara, vertices, triangulos):
                    cubiertos.add(vertice.id)

            cubre_todo = len(cubiertos) == len(vertices)
            print(f"  Cámaras {ids}: cubiertos {sorted(cubiertos)} -> {'Sí' if cubre_todo else 'No'}")

            if cubre_todo:
                mejor = camaras
                break
        if mejor is not None:
            break

    print(f"Óptimo por fuerza bruta: {len(mejor)} cámara(s): {[p.id for p in mejor]}")
    for camara in mejor:
        print(f"  Desde V{camara.id} se ven: {[p.id for p in vertices_cubiertos(camara, vertices, triangulos)]}")
    return list(mejor)

def resolver(nombre, vertices):
    print(f"\n=== {nombre} (n = {len(vertices)}) ===")

    triangulos = brute_force_triangulation(vertices)
    print(f"Triángulos: {len(triangulos)} (esperados: {len(vertices) - 2})")
    for idx, t in enumerate(triangulos):
        print(f"  T{idx + 1}: {t[0].id}, {t[1].id}, {t[2].id}")

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
    L = [Point(0,0,0), Point(4,0,1), Point(4,2,2),
         Point(2,2,3), Point(2,5,4), Point(0,5,5)]
    resolver_minimo_por_fuerza_bruta("Polígono en L", L)

    P8 = [Point(0,0,0), Point(3,0,1), Point(3,2,2), Point(6,2,3),
          Point(6,5,4), Point(4,7,5), Point(2,5,6), Point(0,4,7)]
    resolver_minimo_por_fuerza_bruta("Polígono en P8", P8)
