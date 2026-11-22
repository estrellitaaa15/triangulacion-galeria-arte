# Pruebas de apuntadores y crossProduct
import unittest
from src.dcel import Point, NodoVertice, MediaArista, cross_product


class TestDCEL(unittest.TestCase):
    def test_cross_product(self):
        p1 = Point(0, 0, 0)
        p2 = Point(2, 0, 1)
        p3_izq = Point(1, 1, 2)
        p3_der = Point(1, -1, 3)
        p3_col = Point(4, 0, 4)
        self.assertGreater(cross_product(p1, p2, p3_izq), 0)   # convexo
        self.assertLess(cross_product(p1, p2, p3_der), 0)      # reflejo
        self.assertEqual(cross_product(p1, p2, p3_col), 0)     # alineados

    def test_apuntadores_gemelos(self):
        ab = MediaArista(Point(0, 0, 0))
        ba = MediaArista(Point(1, 0, 1))
        ab.twin = ba
        ba.twin = ab
        self.assertIs(ab.twin.twin, ab)             # twin de twin = la misma
        self.assertEqual(ab.twin.origenP.id, 1)     # origen del gemelo = destino

    def test_nodos_prev_next(self):
        n1 = NodoVertice(Point(0, 0, 0))
        n2 = NodoVertice(Point(1, 0, 1))
        n1.next = n2
        n2.prev = n1
        self.assertIs(n1.next.prev, n1)
        self.assertIsNone(n1.tipoVertice)


if __name__ == '__main__':
    unittest.main()
