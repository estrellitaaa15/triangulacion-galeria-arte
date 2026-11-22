# Pruebas de polígonos pequeños para comprobar la triangulación exhaustiva.
import unittest

from Fuerza_bruta import (
    Point,
    area_poligono,
    construir_grafo_dual,
    cross_product,
    enumerar_triangulaciones_fuerza_bruta,
    seleccionar_camaras,
    tres_coloracion,
    verificar,
)


class TestFuerzaBruta(unittest.TestCase):
    def comprobar_triangulaciones(self, vertices, triangulaciones):
        for triangulos in triangulaciones:
            self.assertEqual(len(triangulos), len(vertices) - 2)

            area_triangular = sum(
                abs(cross_product(*triangulo)) / 2 for triangulo in triangulos
            )
            self.assertAlmostEqual(area_triangular, abs(area_poligono(vertices)))

            dual = construir_grafo_dual(triangulos)
            self.assertEqual(
                sum(len(vecinos) for vecinos in dual.values()) // 2,
                len(vertices) - 3,
            )
            colores = tres_coloracion(triangulos, dual)
            camaras, _ = seleccionar_camaras(colores)
            self.assertEqual(
                verificar(triangulos, colores, camaras, len(vertices)),
                (True, True, True),
            )

    def test_cuadrado(self):
        cuadrado = [
            Point(0, 0, 0),
            Point(2, 0, 1),
            Point(2, 2, 2),
            Point(0, 2, 3),
        ]
        triangulaciones = enumerar_triangulaciones_fuerza_bruta(cuadrado)

        self.assertEqual(len(triangulaciones), 2)
        self.comprobar_triangulaciones(cuadrado, triangulaciones)

    def test_hexagono(self):
        hexagono = [
            Point(1, 0, 0),
            Point(2, 0, 1),
            Point(3, 1, 2),
            Point(2, 2, 3),
            Point(1, 2, 4),
            Point(0, 1, 5),
        ]
        triangulaciones = enumerar_triangulaciones_fuerza_bruta(hexagono)

        self.assertEqual(len(triangulaciones), 14)
        self.comprobar_triangulaciones(hexagono, triangulaciones)

    def test_poligono_de_area_cero(self):
        vertices = [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 2)]

        with self.assertRaises(ValueError):
            enumerar_triangulaciones_fuerza_bruta(vertices)


if __name__ == "__main__":
    unittest.main()
