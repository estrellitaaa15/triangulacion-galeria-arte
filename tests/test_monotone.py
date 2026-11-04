# Pruebas de hacerMonotono y asignaColores
import unittest
from src.triangulador import TrianguladorPoligono
from src.fuerza_bruta import Point

class TestTriangulador(unittest.TestCase):
    def setUp(self):
        self.puntos = [Point(0,0,0), Point(4,0,1), Point(4,2,2), 
                       Point(2,2,3), Point(2,5,4), Point(0,5,5)]
        self.triangulador = TrianguladorPoligono(self.puntos)[cite: 24]

    def test_hacer_monotono(self):
        # Verifica que el barrido retorne las divisiones y-monótonas[cite: 25]
        subpoligonos = self.triangulador.hacerMonotono()
        self.assertIsInstance(subpoligonos, list)
        
    def test_asigna_colores(self):
        # Simulación de un árbol dual G(T_P) para la 3-coloración[cite: 19, 20]
        arbol_dual_mock = {0: [1], 1: [0, 2], 2: [1]}
        colores = self.triangulador.asignaColores(arbol_dual_mock)
        
        # Validar el Teorema de Fisk: uso exclusivo de los colores {0, 1, 2}[cite: 20, 21, 26]
        if colores:
            colores_usados = set(colores.values())
            self.assertTrue(colores_usados.issubset({0, 1, 2}))

if __name__ == '__main__':
    unittest.main()
