from collections import deque

class Point:
    def __init__(self, x, y, id_punto):
        self.x = x
        self.y = y
        self.id = id_punto

    def __repr__(self):
        return f"V{self.id}({self.x}, {self.y})"

def cross_product(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def is_point_in_triangle(pt, v1, v2, v3):

    d1 = cross_product(v1, v2, pt)
    d2 = cross_product(v2, v3, pt)
    d3 = cross_product(v3, v1, pt)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def is_ear(p_prev, p_curr, p_next, polygon):

    if cross_product(p_prev, p_curr, p_next) <= 0:
        return False

    for pt in polygon:
        if pt in (p_prev, p_curr, p_next):
            continue
        if is_point_in_triangle(pt, p_prev, p_curr, p_next):
            return False
    return True

def brute_force_triangulation(vertices):
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
                polygon.pop(i)
                ear_found = True
                break
        
        if not ear_found:
            raise ValueError("Error: Polígono no simple o degenerado.")

    triangles.append((polygon[0], polygon[1], polygon[2]))
    return triangles

def construir_grafo_dual(triangulos):
    adyacencia = {i: [] for i in range(len(triangulos))}
    aristas = {}  

    for i, (a, b, c) in enumerate(triangulos):
        for u, v in ((a, b), (b, c), (c, a)):
            clave = frozenset((u.id, v.id))
            aristas.setdefault(clave, []).append(i)

    for lista in aristas.values():
        if len(lista) == 2:  
            i, j = lista
            adyacencia[i].append(j)
            adyacencia[j].append(i)

    return adyacencia
    
def tres_coloracion(triangulos, adyacencia):
    colores = {}
    a, b, c = triangulos[0]
    colores[a], colores[b], colores[c] = 0, 1, 2    
    
    print(f"Total de triángulos: {len(triangulos)} (Esperados: {len(P)-2})")
    for idx, t in enumerate(triangulos):
        print(f"T{idx+1}: {t[0]}, {t[1]}, {t[2]}")

    visitados = {0}
    fila = deque([0])

    while fila:
        actual = fila.popleft()
        for vecino in adyacencia[actual]:
            if vecino in visitados:
                continue
            visitados.add(vecino)

            colores_usados = {colores[p] for p in triangulos[vecino] if p in colores}
            for p in triangulos[vecinos]:
                if p not in colores:
                    colores[p] = ({0,1,2} - colores_usados).pop()
            fila.append(vecino)

    return colores


def seleccionar_camaras(colores):
    grupos = {0: [], 1: [], 2: []}
    for punto, color in colores.items():
        grupos[color].append(punto)

    mejor = min(grupos, key=lambda c: len(grupos[c]))
    return sorted(grupos[mejor], key=lambda p: p.id), grupos


def verificar(triangulos, colores, camaras, n):
    tres_colores = all(len({colores[p] for p in t}) == 3 for t in triangulos)
    cubiertos = all(any(p in camaras for p in t) for t in triangulos)
    limite = len(camaras) <= n // 3
    return tres_colores, cubiertos, limite



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
