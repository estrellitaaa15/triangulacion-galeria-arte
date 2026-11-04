# Pruebas de clasificarVertices, hacerMonotono y asignaColores
import unittest
from src.dcel import Point, TipoVertice
from src.triangulador import TrianguladorPoligono
from src.fuerza_bruta import brute_force_triangulation


class TestTriangulador(unittest.TestCase):
    def setUp(self):
        self.puntos = [Point(0, 0, 0), Point(4, 0, 1), Point(4, 2, 2),
                       Point(2, 2, 3), Point(2, 5, 4), Point(0, 5, 5)]
        self.triangulador = TrianguladorPoligono(self.puntos)

    def test_clasificar_poligono_L(self):
        tipos = self.triangulador.clasificarVertices()
        self.assertEqual(tipos[5], TipoVertice.START)
        self.assertEqual(tipos[1], TipoVertice.END)
        self.assertNotIn(TipoVertice.SPLIT, tipos.values())
        self.assertNotIn(TipoVertice.MERGE, tipos.values())

    def test_clasificar_split(self):
        v = [Point(0, 0, 0), Point(4, 3, 1), Point(8, 0, 2),
             Point(8, 6, 3), Point(0, 6, 4)]
        tipos = TrianguladorPoligono(v).clasificarVertices()
        self.assertEqual(tipos[1], TipoVertice.SPLIT)

    def test_clasificar_merge(self):
        v = [Point(0, 0, 0), Point(8, 0, 1), Point(8, 6, 2),
             Point(4, 3, 3), Point(0, 6, 4)]
        tipos = TrianguladorPoligono(v).clasificarVertices()
        self.assertEqual(tipos[3], TipoVertice.MERGE)

    def test_hacer_monotono_poligono_L(self):
        # El polígono en L no tiene Split ni Merge: ya es y-monótono
        subpoligonos = self.triangulador.hacerMonotono()
        self.assertIsInstance(subpoligonos, list)
        self.assertEqual(len(subpoligonos), 1)

    def test_punto_repetido(self):
        with self.assertRaises(ValueError):
            TrianguladorPoligono([Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 2)])

    def test_asigna_colores(self):
        # Se usan los triángulos de fuerza bruta mientras se termina el óptimo
        self.triangulador.triangulos = brute_force_triangulation(self.puntos)
        arbol = self.triangulador.construyeGraficaDual()
        colores = self.triangulador.asignaColores(arbol)
        for t in self.triangulador.triangulos:
            self.assertEqual({colores[p] for p in t}, {0, 1, 2})


if __name__ == '__main__':
    unittest.main()
