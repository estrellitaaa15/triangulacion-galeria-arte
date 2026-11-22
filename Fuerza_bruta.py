from collections import deque
from itertools import combinations

class Point:
    def __init__(self, x, y, id_punto):
        self.x = x
        self.y = y
        self.id = id_punto

    def __repr__(self):
        return f"V{self.id}({self.x}, {self.y})"

def cross_product(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


EPSILON = 1e-9


def punto_en_segmento(punto, a, b):
    return (
        abs(cross_product(a, b, punto)) <= EPSILON
        and min(a.x, b.x) - EPSILON <= punto.x <= max(a.x, b.x) + EPSILON
        and min(a.y, b.y) - EPSILON <= punto.y <= max(a.y, b.y) + EPSILON
    )


def segmentos_se_intersectan(a, b, c, d):
    ab_c = cross_product(a, b, c)
    ab_d = cross_product(a, b, d)
    cd_a = cross_product(c, d, a)
    cd_b = cross_product(c, d, b)

    if ((ab_c > EPSILON and ab_d < -EPSILON)
            or (ab_c < -EPSILON and ab_d > EPSILON)):
        if ((cd_a > EPSILON and cd_b < -EPSILON)
                or (cd_a < -EPSILON and cd_b > EPSILON)):
            return True

    return (
        (abs(ab_c) <= EPSILON and punto_en_segmento(c, a, b))
        or (abs(ab_d) <= EPSILON and punto_en_segmento(d, a, b))
        or (abs(cd_a) <= EPSILON and punto_en_segmento(a, c, d))
        or (abs(cd_b) <= EPSILON and punto_en_segmento(b, c, d))
    )


def punto_en_poligono(punto, vertices):
    dentro = False
    for i, a in enumerate(vertices):
        b = vertices[(i + 1) % len(vertices)]
        if punto_en_segmento(punto, a, b):
            return True
        if (a.y > punto.y) != (b.y > punto.y):
            x_interseccion = a.x + (punto.y - a.y) * (b.x - a.x) / (b.y - a.y)
            if punto.x < x_interseccion:
                dentro = not dentro
    return dentro


def diagonal_valida(i, j, vertices):
    n = len(vertices)
    a, b = vertices[i], vertices[j]

    if (i - j) % n in (1, n - 1):
        return False

    for k, c in enumerate(vertices):
        d = vertices[(k + 1) % n]
        comparte_extremo = c in (a, b) or d in (a, b)
        if comparte_extremo:
            otro_extremo = d if c in (a, b) else c
            if otro_extremo not in (a, b) and punto_en_segmento(otro_extremo, a, b):
                return False
        elif segmentos_se_intersectan(a, b, c, d):
            return False

    if any(
        k not in (i, j) and punto_en_segmento(p, a, b)
        for k, p in enumerate(vertices)
    ):
        return False

    medio = Point((a.x + b.x) / 2, (a.y + b.y) / 2, -1)
    return punto_en_poligono(medio, vertices)


def diagonales_se_cruzan(diagonal1, diagonal2, vertices):
    i, j = diagonal1
    k, m = diagonal2
    a, b = vertices[i], vertices[j]
    c, d = vertices[k], vertices[m]

    extremos_compartidos = {i, j} & {k, m}
    if not extremos_compartidos:
        return segmentos_se_intersectan(a, b, c, d)
    if len(extremos_compartidos) == 2:
        return True

    extremo = vertices[next(iter(extremos_compartidos))]
    otro1 = vertices[j if i in extremos_compartidos else i]
    otro2 = vertices[m if k in extremos_compartidos else k]
    colineales = abs(cross_product(extremo, otro1, otro2)) <= EPSILON
    mismo_rayo = (
        (otro1.x - extremo.x) * (otro2.x - extremo.x)
        + (otro1.y - extremo.y) * (otro2.y - extremo.y)
    ) > EPSILON
    return colineales and mismo_rayo


def area_poligono(vertices):
    return sum(
        vertices[i].x * vertices[(i + 1) % len(vertices)].y
        - vertices[(i + 1) % len(vertices)].x * vertices[i].y
        for i in range(len(vertices))
    ) / 2


def triangulos_de_diagonales(vertices, diagonales):
    n = len(vertices)
    aristas = {
        tuple(sorted((i, (i + 1) % n)))
        for i in range(n)
    } | set(diagonales)
    orientacion = 1 if area_poligono(vertices) > 0 else -1
    triangulos = []

    for i, j, k in combinations(range(n), 3):
        if not all(
            tuple(sorted(arista)) in aristas
            for arista in ((i, j), (j, k), (k, i))
        ):
            continue

        a, b, c = vertices[i], vertices[j], vertices[k]
        if orientacion * cross_product(a, b, c) <= EPSILON:
            continue

        if any(
            punto_en_triangulo_estricto(p, a, b, c)
            for indice, p in enumerate(vertices)
            if indice not in (i, j, k)
        ):
            continue

        centroide = Point((a.x + b.x + c.x) / 3,
                          (a.y + b.y + c.y) / 3, -1)
        if punto_en_poligono(centroide, vertices):
            triangulos.append((a, b, c))

    return triangulos


def punto_en_triangulo_estricto(punto, a, b, c):
    productos = (
        cross_product(a, b, punto),
        cross_product(b, c, punto),
        cross_product(c, a, punto),
    )
    return all(valor > EPSILON for valor in productos) or all(
        valor < -EPSILON for valor in productos
    )


def enumerar_triangulaciones_fuerza_bruta(vertices):
    n = len(vertices)
    if n < 3 or abs(area_poligono(vertices)) <= EPSILON:
        raise ValueError("Se necesita un polígono con al menos 3 vértices y área.")

    diagonales = [
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if diagonal_valida(i, j, vertices)
    ]
    triangulaciones = []

    for conjunto in combinations(diagonales, n - 3):
        if any(
            diagonales_se_cruzan(d1, d2, vertices)
            for d1, d2 in combinations(conjunto, 2)
        ):
            continue

        triangulos = triangulos_de_diagonales(vertices, conjunto)
        area_triangular = sum(
            abs(cross_product(*triangulo)) / 2 for triangulo in triangulos
        )
        if (len(triangulos) == n - 2
                and abs(area_triangular - abs(area_poligono(vertices))) <= EPSILON):
            triangulaciones.append(triangulos)

    if not triangulaciones:
        raise ValueError("No se encontraron triangulaciones válidas.")
    return triangulaciones

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

    visitados = {0}
    fila = deque([0])

    while fila:
        actual = fila.popleft()
        for vecino in adyacencia[actual]:
            if vecino in visitados:
                continue
            visitados.add(vecino)

            colores_usados = {colores[p] for p in triangulos[vecino] if p in colores}
            color_disponible = {0, 1, 2} - colores_usados
            for p in triangulos[vecino]:
                if p not in colores:
                    colores[p] = color_disponible.pop()
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

    triangulaciones = enumerar_triangulaciones_fuerza_bruta(vertices)
    print(f"Triangulaciones válidas examinadas: {len(triangulaciones)}")

    mejor = None
    for triangulos_candidatos in triangulaciones:
        adyacencia_candidata = construir_grafo_dual(triangulos_candidatos)
        colores_candidatos = tres_coloracion(
            triangulos_candidatos, adyacencia_candidata)
        camaras_candidatas, _ = seleccionar_camaras(colores_candidatos)
        if mejor is None or len(camaras_candidatas) < len(mejor[2]):
            mejor = (triangulos_candidatos, adyacencia_candidata,
                     camaras_candidatas, colores_candidatos)

    triangulos, adyacencia, camaras, colores = mejor
    print(f"Triángulos: {len(triangulos)} (esperados: {len(vertices) - 2})")

    aristas_dual = sum(len(v) for v in adyacencia.values()) // 2
    print(f"Árbol dual: {len(triangulos)} nodos, {aristas_dual} aristas "
          f"(esperadas: {len(vertices) - 3})")
    for i, vecinos in adyacencia.items():
        print(f"  T{i + 1} -> {['T' + str(j + 1) for j in vecinos]}")

    _, grupos = seleccionar_camaras(colores)
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
