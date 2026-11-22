#Importa el módulo estándar de pruebas unitarias, todas las clases del algoritmo óptimo y los generadores de polígonos
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

#Suite de pruebas unitarias que valida de forma aislada cada estructura de datos, regla geométrica y caso límite
class TestAlgoritmoOptimo(unittest.TestCase):

    def test_estructuras_auxiliares_queue_y_bst(self):
        #Comprueba que la cola respete el orden FIFO (primero en entrar, primero en salir) y actualice su tamaño
        cola = ArrayQueue()
        self.assertTrue(cola.is_empty())
        cola.enqueue("A")
        cola.enqueue("B")
        self.assertEqual(cola.first(), "A")
        self.assertEqual(cola.dequeue(), "A")
        self.assertEqual(len(cola), 1)

        #Verificar búsqueda izquierda en BST con arista inclinada
        #Toma la arista izquierda inclinada del polígono y confirma que el BST la detecta a la izquierda de x=3.0
        dcel = DCEL([Point(0, 0), Point(6, 0), Point(4, 6), Point(0, 6)])
        aristaIzq = [a for a in dcel.mediasAristas if a.trianguloPertenece == 0 and a.origenP.x == 0 and a.origenP.y == 6][0]
        bst = BST()
        bst.insertar(aristaIzq, 6.0)
        encontrada = bst.buscarIzquierda(3.0, 3.0)
        self.assertIs(encontrada, aristaIzq)

    def test_cross_product_y_dcel(self):
        #Evalúa el determinante del producto cruz para distinguir giros a la izquierda, giros a la derecha y puntos alineados
        p1 = Point(0, 0)
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        self.assertGreater(Point.crossProduct(p1, p2, Point(2, 3)), 0)   # Giro antihorario (convexo)
        self.assertLess(Point.crossProduct(p1, p2, Point(2, -3)), 0)     # Giro horario (reflejo)
        self.assertEqual(Point.crossProduct(p1, p2, Point(8, 0)), 0)     # Colineales

        #Verificar lista doblemente ligada circular y aristas gemelas (twin)
        #Comprueba que los 4 nodos estén enlazados en círculo y que cada media arista apunte a su gemela opuesta (twin)
        dcel = DCEL([Point(0, 0), Point(4, 0), Point(4, 4), Point(0, 4)])
        self.assertEqual(len(dcel.nodosCircular), 4)
        for arista in dcel.mediasAristas:
            self.assertIs(arista.twin.twin, arista)

        #Insertar diagonal divide el cuadrado en 2 triángulos
        #Traza una diagonal entre vértices opuestos y verifica que la DCEL divida el cuadrado en 2 caras independientes
        dcel.masDiagonal(dcel.verticesP[0], dcel.verticesP[2])
        self.assertEqual(len(dcel.extraerSubpoligonos()), 2)

    def test_clasificacion_5_tipos_vertices(self):
        #Rombo para START (arriba) y END (abajo)
        #Usa un rombo para comprobar que el vértice más alto sea START, el más bajo sea END y los laterales sean REGULAR
        rombo = [Point(0, 2), Point(2, 0), Point(4, 2), Point(2, 4)]
        tiposRombo = TrianguladorPoligono(rombo).clasificarVertices()
        self.assertEqual(tiposRombo[rombo[3]], TipoVertice.START)
        self.assertEqual(tiposRombo[rombo[1]], TipoVertice.END)
        self.assertEqual(tiposRombo[rombo[0]], TipoVertice.REGULAR)

        #Polígono con vértice SPLIT estricto
        #Crea un pico reflejo apuntando hacia adentro desde arriba para validar la detección de vértices MERGE
        poliSplit = [Point(0, 0), Point(4, 3), Point(8, 0), Point(8, 6), Point(0, 6)]
        tiposSplit = TrianguladorPoligono(poliSplit).clasificarVertices()
        self.assertEqual(tiposSplit[poliSplit[1]], TipoVertice.SPLIT)

        # Polígono con vértice MERGE estricto
        poliMerge = [Point(0, 0), Point(8, 0), Point(8, 6), Point(4, 3), Point(0, 6)]
        tiposMerge = TrianguladorPoligono(poliMerge).clasificarVertices()
        self.assertEqual(tiposMerge[poliMerge[3]], TipoVertice.MERGE)

    def test_poligono_L_fase1(self):
        #Ejemplo de 6 vértices del protocolo experimental
        #Ejecuta todo el algoritmo sobre el polígono en L de 6 vértices y revisa el conteo de triángulos y cámaras
        poligonoL = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 5), (0, 5)]
        res = triangularPoligono(poligonoL)

        self.assertEqual(res["nVertices"], 6)
        self.assertEqual(len(res["triangulos"]), 4)     #n - 2 = 4 triángulos
        self.assertLessEqual(len(res["camaras"]), 2)    #floor(6 / 3) = 2 cámaras

        #Verificar que ningún triángulo repita colores (3-coloración válida)
        #Recorre cada triángulo formado para confirmar que sus 3 vértices tengan colores distintos ({0, 1, 2})
        colores = res["diccPoint"]
        for t in res["triangulos"]:
            self.assertEqual({colores[v] for v in t}, {0, 1, 2})

    def test_poligonos_mas_de_100_vertices(self):
        #Caso 1: Peine de Chvátal de 40 dientes = 120 vértices (exige exactamente n/3 = 40 cámaras)
        #Evalúa el peor caso teórico con 120 vértices (3 + 3*39), donde el algoritmo debe asignar exactamente 40 cámaras
        peine120 = generarPoligonoPeine(39)
        resPeine = triangularPoligono(peine120)
        self.assertEqual(resPeine["nVertices"], 120)
        self.assertEqual(len(resPeine["triangulos"]), 118)
        self.assertEqual(len(resPeine["camaras"]), 40)

        #Caso 2: Polígono estrella aleatorio de 250 vértices
        #Evalúa la escalabilidad en un polígono estrella de 250 vértices verificando n-2 triángulos y la cota de Fisk
        estrella250 = generarPoligonoEstrella(n=250, seed=42)
        resEstrella = triangularPoligono(estrella250)
        self.assertEqual(resEstrella["nVertices"], 250)
        self.assertEqual(len(resEstrella["triangulos"]), 248)
        self.assertLessEqual(len(resEstrella["camaras"]), 250 // 3)

    def test_excepciones_entradas_invalidas(self):
        #Verifica que el validador rechace polígonos degenerados o no simples lanzando ErrorPoligonoInvalido
        #Menos de 3 vértices
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (2, 2)])

        #Vértice duplicado
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (4, 0), (0, 0)])

        #Polígono auto-intersecante (aristas cruzadas)
        with self.assertRaises(ErrorPoligonoInvalido):
            triangularPoligono([(0, 0), (4, 4), (0, 4), (4, 0)])

#Punto de entrada para ejecutar todas las pruebas al correr 'python -m unittest tests.test_algoritmo_optimo -v'
if __name__ == "__main__":
    unittest.main()