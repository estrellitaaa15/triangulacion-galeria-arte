# Pruebas de creación de un polígono pequeño (como un cuadrado o hexágono) 
# para saber si el algoritmo de fuerza bruta logra triangularlo sin fallas
import unittest
from src.fuerza_bruta import Point, brute_force_triangulation

class TestFuerzaBruta(unittest.TestCase):
    def test_cuadrado(self):
        # Polígono de 4 vértices
        cuadrado = [Point(0, 0, 0), Point(2, 0, 1), Point(2, 2, 2), Point(0, 2, 3)]
        triangulos = brute_force_triangulation(cuadrado)
        self.assertEqual(len(triangulos), 2) # n-2 triángulos[cite: 4, 27]
        
    def test_hexagono(self):
        # Polígono de 6 vértices
        hexagono = [Point(1, 0, 0), Point(2, 0, 1), Point(3, 1, 2), 
                    Point(2, 2, 3), Point(1, 2, 4), Point(0, 1, 5)]
        triangulos = brute_force_triangulation(hexagono)
        self.assertEqual(len(triangulos), 4) # n-2 triángulos[cite: 6, 27]

if __name__ == '__main__':
    unittest.main()
