# Clase principal: TrianguladorPoligono
from src.dcel import TipoVertice, cross_product
from src.fuerza_bruta import (construir_grafo_dual, tres_coloracion,
                              seleccionar_camaras)


def esta_debajo(a, b):
    """a está 'debajo' de b si tiene menor y (o igual y, y mayor x)."""
    return a.y < b.y or (a.y == b.y and a.x > b.x)


class TrianguladorPoligono:
    def __init__(self, poligono, dcel=None, diagonales=None, triangulos=None):
        ids = [p.id for p in poligono]
        if len(ids) != len(set(ids)):
            raise ValueError("Hay puntos repetidos (mismo id) en el polígono")
        self.poligono = poligono          # vértices en orden antihorario
        self.dcel = dcel
        self.diagonales = diagonales if diagonales is not None else []
        self.triangulos = triangulos if triangulos is not None else []
        self.tipos = {}

    def clasificarVertices(self):
        """Regresa {id_vertice: TipoVertice} usando el producto cruz."""
        n = len(self.poligono)
        for i in range(n):
            prev = self.poligono[i - 1]
            v = self.poligono[i]
            sig = self.poligono[(i + 1) % n]
            convexo = cross_product(prev, v, sig) > 0
            prev_abajo = esta_debajo(prev, v)
            sig_abajo = esta_debajo(sig, v)

            if prev_abajo and sig_abajo:
                tipo = TipoVertice.START if convexo else TipoVertice.SPLIT
            elif not prev_abajo and not sig_abajo:
                tipo = TipoVertice.END if convexo else TipoVertice.MERGE
            else:
                tipo = TipoVertice.REGULAR
            self.tipos[v.id] = tipo
        return self.tipos

    def hacerMonotono(self):
        """Regresa la lista de sub-polígonos y-monótonos."""
        tipos = self.clasificarVertices()
        hay_split_merge = any(t in (TipoVertice.SPLIT, TipoVertice.MERGE)
                              for t in tipos.values())
        if not hay_split_merge:
            return [self.poligono]        # ya es y-monótono
        raise NotImplementedError("PENDIENTE: barrido de plano con diagonales")

    def triangularPoligonoMonotono(self, yMonotono):
        raise NotImplementedError("PENDIENTE: triangulación con pila")

    def construyeGraficaDual(self):
        return construir_grafo_dual(self.triangulos)

    def asignaColores(self, arbolDual):
        return tres_coloracion(self.triangulos, arbolDual)

    def seleccionarUbicacion(self, diccPoint):
        camaras, _ = seleccionar_camaras(diccPoint)
        return camaras