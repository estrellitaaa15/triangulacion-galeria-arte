import unittest
from src.algoritmo_optimo import (
    ArrayQueue,
    BST,
    Point,
    TipoVertice,
    NodoVertice,
    MediaArista,
    DCEL,
    TrianguladorPoligono,
    ErrorPoligonoInvalido,
    triangularPoligono,
)
from src.generador_poligonos import generarPoligonoEstrella, generarPoligonoPeine


class TestAlgoritmoOptimo(unittest.TestCase):

    def test_estructuras_auxiliares_queue_y_bst(self):
        cola = ArrayQueue()
        self.assertTrue(cola.is_empty())
        cola.enqueue("A")
        cola.enqueue("B")
        self.assertEqual(cola.first(), "A")
        self.assertEqual(cola.dequeue(), "A")
        self.assertEqual(len(cola), 1)

        # Verificar búsqueda izquierda en BST con arista inclinada
        dcel = DCEL([Point(0, 0), Point(6, 0), Point(4, 6), Point(0, 6)])
        aristaIzq = [a for a in dcel.mediasAristas if a.trianguloPertenece == 0 and a.origenP.x == 0 and a.origenP.y == 6][0]
        bst = BST()
        bst.insertar(aristaIzq, 6.0)
        encontrada = bst.buscarIzquierda(3.0, 3.0)
        self.assertIs(encontrada, aristaIzq)

    def test_cross_product_y_dcel(self):
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        self.assertGreater(Point.crossProduct(p1, p2, Point(2, 3)), 0)   # Giro antihorario (convexo)
        self.assertLess(Point.crossProduct(p1, p2, Point(2, -3)), 0)     # Giro horario (reflejo)
        self.assertEqual(Point.crossProduct(p1, p2, Point(8, 0)), 0)     # Colineales

        # Verificar lista doblemente ligada circular y aristas gemelas (twin)
        dcel = DCEL([Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)])
        self.assertEqual(len(dcel.nodosCircular), 4)
        for arista in dcel.mediasAristas:
            self.assertIs(arista.twin.twin, arista)

        # Insertar diagonal divide el cuadrado en 2 triángulos
        dcel.masDiagonal(dcel.verticesP[0], dcel.verticesP[2])
        self.assertEqual(len(dcel.extraerSubpoligonos()), 2)

    def test_clasificacion_5_tipos_vertices(self):
        # Rombo para START (arriba) y END (abajo)
        rombo = [Point(0, 2), Point(2, 0), Point(4, 2), Point(2, 4)]
        tiposRombo = TrianguladorPoligono(rombo).clasificarVertices()
        self.assertEqual(tiposRombo[rombo[3]], TipoVertice.START)
        self.assertEqual(tiposRombo[rombo[1]], TipoVertice.END)
        self.assertEqual(tiposRombo[rombo[0]], TipoVertice.REGULAR)

        # Polígono con vértice SPLIT estricto
        poliSplit = [Point(0, 0), Point(4, 3), Point(8, 0), Point(8, 6), Point(0, 6)]
        tiposSplit = TrianguladorPoligono(poliSplit).clasificarVertices()
        self.assertEqual(tiposSplit[poliSplit[1]], TipoVertice.SPLIT)

        # Polígono con vértice MERGE estricto
        poliMerge = [Point(0, 0), Point(8, 0), Point(8, 6), Point(4, 3), Point(0, 6)]
        tiposMerge = TrianguladorPoligono(poliMerge).clasificarVertices()
        self.assertEqual(tiposMerge[poliMerge[3]], TipoVertice.MERGE)

    def test_poligono_L_fase1(self):
        # Ejemplo de 6 vértices del protocolo experimental
        poligonoL = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)]
        res = triangularPoligono(poligonoL)

        self.assertEqual(res["nVertices"], 6)
        self.assertEqual(len(res["triangulos"]), 4)     # n - 2 = 4 triángulos
        self.assertLessEqual(len(res["camaras"]), 2)    # floor(6 / 3) = 2 cámaras

        # Verificar que ningún triángulo repita colores (3-coloración válida)
        colores = res["diccPoint"]
        for t in res["triangulos"]:
            self.assertEqual({colores[v] for v in t}, {0, 1, 2})

    def test_poligonos_mas_de_100_vertices(self):
        # Caso 1: Peine de Chvátal de 40 dientes = 120 vértices (exige exactamente n/3 = 40 cámaras)
        peine120 = generarPoligonoPeine(39)
        resPeine = triangularPoligono(peine120)
        self.assertEqual(resPeine["nVertices"], 120)
        self.assertEqual(len(resPeine["triangulos"]), 118)
        self.assertEqual(len(resPeine["camaras"]), 40)

        # Caso 2: Polígono estrella aleatorio de 250 vértices
        estrella250 = generarPoligonoEstrella(n=250, seed=42)
        resEstrella = triangularPoligono(estrella250)
        self.assertEqual(resEstrella["nVertices"], 250)
        self.assertEqual(len(resEstrella["triangulos"]), 248)
        self.assertLessEqual(len(resEstrella["camaras"]), 250 // 3)

    def test_excepciones_entradas_invalidas(self):
        # Menos de 3 vértices
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (2, 2)])

        # Vértice duplicado
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (4, 0), (0, 0)])

        # Polígono auto-intersecante (aristas cruzadas)
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (4, 4), (0, 4), (4, 0)])


if __name__ == "__main__":
    unittest.main()