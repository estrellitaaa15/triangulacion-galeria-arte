# Pruebas de polígonos pequeños para comprobar la triangulación exhaustiva.
# sirve para automatizar pruebas y aserciones
import unittest
# Importar las clases y funciones del módulo de fuerza bruta a evaluar
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

# Pruebas unitarias sobre polígonos conocidos y casos límite
class TestFuerzaBruta(unittest.TestCase):
    # Valida las propiedad geométricas y de vigilancia de cada triangulación
    def comprobar_triangulaciones(self, vertices, triangulaciones):
        for triangulos in triangulaciones:
            # Todo polígono de n vértices debe partirse exactamente n-2 triángulos
            self.assertEqual(len(triangulos), len(vertices) - 2)

            # La suma de áreas de los triángulos debe igualar el área total del polígono
            area_triangular = sum(
                abs(cross_product(*triangulo)) / 2 for triangulo in triangulos
            )
            self.assertAlmostEqual(area_triangular, abs(area_poligono(vertices)))

            # El árbol dual de la triangulación debe tener exactamente n -3 aristas
            dual = construir_grafo_dual(triangulos)
            self.assertEqual(
                sum(len(vecinos) for vecinos in dual.values()) // 2,
                len(vertices) - 3,
            )
            # El 3-coloreo y las cámaras deben cubrir todo el polígono
            colores = tres_coloracion(triangulos, dual)
            camaras, _ = seleccionar_camaras(colores)
            self.assertEqual(
                verificar(triangulos, colores, camaras, len(vertices)),
                (True, True, True),
            )

# Verifica que un cuadrado produzca exactamente 2 triangulaciones
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

# Verifica que un hexágono convexo produzca exactamente 14 triangulaciones
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

# Verifica que se lance ValueError ante vértices colineales sin área
    def test_poligono_de_area_cero(self):
        vertices = [Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 2)]

        with self.assertRaises(ValueError):
            enumerar_triangulaciones_fuerza_bruta(vertices)

# Ejecutar todas las pruebas definidas en la clase
if __name__ == "__main__":
    unittest.main()
