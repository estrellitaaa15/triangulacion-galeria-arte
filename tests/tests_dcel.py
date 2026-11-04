# # Pruebas de apuntadores y crossProduct
import unittest
from src.dcel import Point, NodoVertice, MediaArista
from src.fuerza_bruta import cross_product 

class TestDCEL(unittest.TestCase):
    def test_cross_product(self):
        p1 = Point(0, 0, 0)
        p2 = Point(2, 0, 1)
        p3_izq = Point(1, 1, 2)
        p3_der = Point(1, -1, 3)
        p3_col = Point(4, 0, 4)
        
        # Giro a la izquierda (convexo, Det > 0)[cite: 12, 23]
        self.assertTrue(cross_product(p1, p2, p3_izq) > 0)
        # Giro a la derecha (reflejo, Det < 0)[cite: 12, 23]
        self.assertTrue(cross_product(p1, p2, p3_der) < 0)
        # Puntos alineados (Det = 0)[cite: 12, 23]
        self.assertEqual(cross_product(p1, p2, p3_col), 0)

    def test_apuntadores_gemelos(self):
        # Validación de la interconexión DCEL
        nodo1 = NodoVertice(Point(0,0,0))
        nodo2 = NodoVertice(Point(1,0,1))
        
        arista = MediaArista(nodo1)
        arista_twin = MediaArista(nodo2)
        
        arista.twin = arista_twin
        arista_twin.twin = arista
        
        # El origen del gemelo debe ser el destino de la arista original[cite: 14]
        self.assertEqual(arista.twin.origen.id, 1) 
        
if __name__ == '__main__':
    unittest.main()
