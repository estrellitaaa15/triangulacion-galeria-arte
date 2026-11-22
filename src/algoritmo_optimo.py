# Librerias
from enum import Enum, unique
from typing import Optional
import math

#EXCEPCIONES (VALIDACIÓN DE ENTRADAS Y TOPOLOGÍA)
class Empty(Exception):
    """Excepción lanzada cuando se intenta extraer de una estructura vacía."""
    pass


class ErrorPoligonoInvalido(Exception):
    """Excepción lanzada si el polígono tiene menos de 3 vértices, puntos repetidos,
    vértices colineales consecutivos o aristas que se auto-intersectan."""
    pass


class ErrorGeometriaDCEL(Exception):
    """Excepción lanzada ante inconsistencias topológicas al conectar medias aristas o diagonales."""
    pass


class ErrorTriangulacion(Exception):
    """Excepción lanzada si ocurre un error durante la partición monótona, triangulación o coloración."""
    pass


#ESTRUCTURAS AUXILIARES: COLA (ARRAYQUEUE) Y ÁRBOL DE ESTADO (BST)
#class ArrayQueue proviene de los ejercicios de clase 
class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 8  # moderate capacity for all new queues

    def __init__(self):
        """Create an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue.
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO).
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None          # help garbage collection
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))   # double the array size
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        """Resize to a new list of capacity >= len(self)."""
        old = self._data                         # keep track of existing list
        self._data = [None] * cap                # allocate list with new capacity
        walk = self._front
        for k in range(self._size):              # only consider existing elements
            self._data[k] = old[walk]            # intentionally shift indices
            walk = (walk + 1) % len(old)         # use old size as modulus
        self._front = 0                          # front has been reset

    def _mostrar(self):
        print(self._data)

    def __getitem__(self, k):
        if not 0 <= k < self._size:
            raise IndexError('Índice fuera de rango')
        index = (self._front + k) % len(self._data)
        return self._data[index]


class NodoBST:
    __slots__ = 'arista', 'izq', 'der'

    def __init__(self, arista: 'MediaArista'):
        self.arista = arista
        self.izq = None
        self.der = None


class BST:
    def __init__(self):
        self.raiz = None

    def _evaluar_x(self, arista: 'MediaArista', y_actual: float) -> float:
        #En un barrido real, x cambia según la altura y.
        #Calcular la intersección x de la arista a la altura y_actual.
        #Usa la ecuación de la recta entre p1 y p2 para saber exactamente en qué coordenada X corta la línea de barrido horizontal y_actual.
        p1 = arista.origenP
        p2 = arista.next.origenP
        if abs(p1.y - p2.y) < 1e-12:
            return min(p1.x, p2.x)
        return p1.x + (y_actual - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
    #Ubica la arista activa de izquierda a derecha comparando su coordenada X evaluada a la altura actual del barrido.
    def insertar(self, arista: 'MediaArista', y_actual: float):
        if self.raiz is None:
            self.raiz = NodoBST(arista)
            return

        actual = self.raiz
        x_nueva = self._evaluar_x(arista, y_actual)

        while True:
            x_actual = self._evaluar_x(actual.arista, y_actual)
            if x_nueva < x_actual:
                if actual.izq is None:
                    actual.izq = NodoBST(arista)
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = NodoBST(arista)
                    break
                actual = actual.der

    def buscarIzquierda(self, x_vertice: float, y_actual: float) -> Optional['MediaArista']:
        #Encuentra la arista activa (arista que toca la linea) inmediatamente a la izquierda del vértice actual (v.x)
        actual = self.raiz
        mejor_opcion = None
        #Busqueda de vecino a la izquierda: Si la arista está a la izquierda (x_actual < x_vertice), la guarda como candidata y baja a la derecha buscando otra aún más cercana al vértice
        while actual is not None:
            x_actual = self._evaluar_x(actual.arista, y_actual)

            if x_actual < x_vertice - 1e-12:
                mejor_opcion = actual.arista
                actual = actual.der  #Buscar si hay otra arista más cercana por la derecha
            else:
                actual = actual.izq

        return mejor_opcion

    def eliminar(self, arista: 'MediaArista'):
        #Para la eliminación estándar de un BSTse usa un método auxiliar recursivo
        self.raiz = self._eliminar_nodo(self.raiz, arista)

    def _eliminar_nodo(self, nodo: Optional['NodoBST'], arista: 'MediaArista') -> Optional['NodoBST']:
        if nodo is None:
            return None

        if arista is nodo.arista:
            #Caso 1 y 2: Sin hijos o un solo hijo
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq

            #Caso 3: Dos hijos. Buscar el sucesor (el menor del subárbol derecho)
            sucesor = nodo.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            nodo.arista = sucesor.arista
            nodo.der = self._eliminar_nodo(nodo.der, sucesor.arista)
        else:
            nodo.izq = self._eliminar_nodo(nodo.izq, arista)
            nodo.der = self._eliminar_nodo(nodo.der, arista)

        return nodo

#CLASES BASE GEOMÉTRICAS Y TOPOLÓGICAS (DISEÑO METODOLÓGICO)
class Point:
    verticeID = 0

    def __init__(self, x: float, y: float):
        #Validación de coordenadas: Bloquea booleanos, textos o valores infinitos, y asigna automáticamente un identificador único consecutivo (idVertice).
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ErrorPoligonoInvalido(f"Las coordenadas deben ser numéricas, se recibió: ({x}, {y})")
        if math.isnan(x) or math.isnan(y) or math.isinf(x) or math.isinf(y):
            raise ErrorPoligonoInvalido("Las coordenadas no pueden ser NaN ni infinitas.")

        Point.verticeID += 1
        self.idVertice = Point.verticeID
        self.color = None
        self.x = float(x)
        self.y = float(y)
    #Método para comprar coordenadas en base a su y para el barrido más adelante (en base a altura mayor), si empatan en altura Y, va primero el que esté más a la izquierda (menor X).
    def __lt__(self, P: 'Point') -> bool:  #P son los objetos tipo Point
        if self.y == P.y:
            return self.x < P.x
        return self.y > P.y
    #Da un formato más limpio para imprimir el vértice como V1(x, y) en consola y pruebas
    def __repr__(self) -> str:
        return f"V{self.idVertice}({self.x}, {self.y})"

    @staticmethod  #Permite ejecutar el método directamente desde la clase sin necesidad de instanciar un objeto
    def crossProduct(P1: 'Point', P2: 'Point', P3: 'Point') -> float:
        return (P2.x - P1.x) * (P3.y - P1.y) - (P2.y - P1.y) * (P3.x - P1.x)
        # Det positiva: giro izq
        # Det negativa: giro der
        # Det 0: recta


@unique  #Todos los valores de la enumeración únicos
class TipoVertice(Enum): #Enumeración de los diferentes tipos de vértices
    START = 1
    END = 2
    SPLIT = 3
    MERGE = 4
    REGULAR = 5


class NodoVertice:
    __slots__ = 'P', 'prev', 'next', 'tipoVertice'

    def __init__(self, P: Point, prev: Optional['NodoVertice'] = None, next: Optional['NodoVertice'] = None):
        self.P = P  #Objeto Point
        self.tipoVertice = None
        self.prev = prev
        self.next = next


class MediaArista:
    __slots__ = 'origenP', 'twin', 'next', 'prev', 'trianguloPertenece'

    def __init__(self, origenP: Point):
        self.origenP = origenP  #De que vértice nace la arista
        self.trianguloPertenece = None
        self.twin = None
        self.next = None
        self.prev = None
        #next -> siguiente media arista
        #prev -> media arista anterior


class DCEL:
    def __init__(self, verticesP: list['Point'], mediasAristas: Optional[list['MediaArista']] = None, caras: Optional[list] = None):
        if verticesP is None or len(verticesP) < 3:
            raise ErrorPoligonoInvalido("Se requieren al menos 3 vértices para construir una DCEL.")
        #Garantiza recorrido antihorario, arma la lista doblemente ligada circular de vértices y crea las medias aristas iniciales.
        self.verticesP = self._asegurarAntihorario(verticesP)
        self.nodosCircular = self._construirListaCircular(self.verticesP)

        if mediasAristas is not None and caras is not None and len(mediasAristas) > 0:
            self.mediasAristas = mediasAristas
            self.caras = caras
        else:
            self.mediasAristas = []
            self.caras = []
            self._construirCicloInicial()
    #Orientación antihoraria del poligono, Usa la fórmula del área con signo (Shoelace): si el área es negativa (sentido horario), invierte la lista de vértices.
    @staticmethod
    def _asegurarAntihorario(puntos: list['Point']) -> list['Point']:
        n = len(puntos)
        areaDoble = 0.0
        for i in range(n):
            p1 = puntos[i]
            p2 = puntos[(i + 1) % n]
            areaDoble += (p1.x * p2.y - p2.x * p1.y)
        if abs(areaDoble) < 1e-12:
            raise ErrorPoligonoInvalido("El polígono tiene área cero (vértices degenerados).")
        return list(reversed(puntos)) if areaDoble < 0 else list(puntos)
    #Lista doblemente ligada circular que conecta cada nodo con su vecino anterior y siguiente
    @staticmethod
    def _construirListaCircular(puntos: list['Point']) -> list['NodoVertice']:
        n = len(puntos)
        nodos = [NodoVertice(p) for p in puntos]
        for i in range(n):
            nodos[i].next = nodos[(i + 1) % n]
            nodos[i].prev = nodos[(i - 1) % n]
        return nodos
    #Crea dos flechas opuestas (twin) por cada pared, una recorre el interior en sentido antihorario (cara 0) y otra el exterior en horario.
    def _construirCicloInicial(self):
        n = len(self.verticesP)
        aristasInt = [MediaArista(self.verticesP[i]) for i in range(n)]
        aristasExt = [MediaArista(self.verticesP[(i + 1) % n]) for i in range(n)]

        for i in range(n):
            sig = (i + 1) % n
            ant = (i - 1) % n

            #Contorno interior en sentido antihorario (cara 0)
            aristasInt[i].next = aristasInt[sig]
            aristasInt[i].prev = aristasInt[ant]
            aristasInt[i].twin = aristasExt[i]
            aristasInt[i].trianguloPertenece = 0

            #Contorno exterior en sentido horario (cara externa None)
            aristasExt[i].next = aristasExt[ant]
            aristasExt[i].prev = aristasExt[sig]
            aristasExt[i].twin = aristasInt[i]
            aristasExt[i].trianguloPertenece = None

        self.mediasAristas.extend(aristasInt)
        self.mediasAristas.extend(aristasExt)
        self.caras.append(aristasInt[0])

    def masDiagonal(self, P1: Point, P2: Point):
        if P1 is P2:
            raise ErrorGeometriaDCEL("No se puede trazar una diagonal de un vértice hacia sí mismo.")

        #Arista dirigida de A -> B y de B -> A
        diagonalAB = MediaArista(P1)
        diagonalBA = MediaArista(P2)
        #Uso de twin para relacionarlas
        diagonalAB.twin = diagonalBA
        diagonalBA.twin = diagonalAB

        #Encontrar medias aristas que salen de cada vértice y comparten la misma cara interior
        salidasP1 = [a for a in self.mediasAristas if a.origenP is P1 and a.trianguloPertenece is not None]
        salidasP2 = [a for a in self.mediasAristas if a.origenP is P2 and a.trianguloPertenece is not None]

        aristaSalidaP1 = None
        aristaSalidaP2 = None
        for a1 in salidasP1:
            for a2 in salidasP2:
                if a1.trianguloPertenece == a2.trianguloPertenece:
                    aristaSalidaP1 = a1
                    aristaSalidaP2 = a2
                    break
            if aristaSalidaP1 is not None:
                break

        if aristaSalidaP1 is None or aristaSalidaP2 is None:
            raise ErrorGeometriaDCEL(f"No se encontró una cara común entre {P1} y {P2} para insertar la diagonal.")

        #Aristas que llegan a los vértices
        aristaEntP1 = aristaSalidaP1.prev
        aristaEntP2 = aristaSalidaP2.prev

        #Conectar diagonal de P1 -> P2
        aristaEntP1.next = diagonalAB
        diagonalAB.prev = aristaEntP1
        diagonalAB.next = aristaSalidaP2
        aristaSalidaP2.prev = diagonalAB

        #Conectar diagonal de P2 -> P1
        aristaEntP2.next = diagonalBA
        diagonalBA.prev = aristaEntP2
        diagonalBA.next = aristaSalidaP1
        aristaSalidaP1.prev = diagonalBA

        #Actualizar caras resultantes de la división
        #Se dividen las regiones, al cerrar dos ciclos independientes, recorre ambos con .next para etiquetar cada subpolígono con su propio identificador de cara.
        caraOriginal = aristaSalidaP1.trianguloPertenece
        nuevaCara = len(self.caras)

        actual = diagonalAB
        while True:
            actual.trianguloPertenece = caraOriginal
            actual = actual.next
            if actual is diagonalAB:
                break

        actual = diagonalBA
        while True:
            actual.trianguloPertenece = nuevaCara
            actual = actual.next
            if actual is diagonalBA:
                break

        self.caras[caraOriginal] = diagonalAB
        self.caras.append(diagonalBA)

        #Agregar las nuevas aristas a la lista de la clase
        self.mediasAristas.append(diagonalAB)
        self.mediasAristas.append(diagonalBA)
    #Recorre los punteros .next de cada cara guardada en self.caras para devolver cada subpolígono como una lista limpia de vértices
    def extraerSubpoligonos(self) -> list[list['Point']]:
        #Extrae cada cara interior de la DCEL como una lista ordenada de objetos Point.
        subpoligonos = []
        for aristaInicio in self.caras:
            poligonoCara = []
            actual = aristaInicio
            while True:
                poligonoCara.append(actual.origenP)
                actual = actual.next
                if actual is aristaInicio:
                    break
            subpoligonos.append(poligonoCara)
        return subpoligonos


#ALGORITMO PRINCIPAL: TRIANGULACIÓN Y 3-COLORACIÓN (TEOREMA DE FISK)
class TrianguladorPoligono:
    def __init__(self, dcel: 'DCEL'):
        if isinstance(dcel, list):
            dcel = DCEL(dcel)
        if not isinstance(dcel, DCEL):
            raise ErrorPoligonoInvalido("Se esperaba un objeto DCEL o una lista de objetos Point.")

        self.operaciones = 0
        self.dcel = dcel
        self.diagonales = []
        self.triangulos = []

    def clasificarVertices(self) -> dict:
        clasificacionVertices = {}
        #Clasificación de los vértices dentro de los 5 tipos definidos, Evalúa únicamente el contorno interior (cara 0). 
        #Combina la altura relativa (<) con el signo del producto cruz (>0 convexo, <0 reflejo).
        for arista in self.dcel.mediasAristas:
            if arista.trianguloPertenece != 0:
                continue

            aristaPrev = arista.prev.origenP
            aristaActual = arista.origenP
            aristaNext = arista.next.origenP
            self.operaciones += 1
            determinante = Point.crossProduct(aristaPrev, aristaActual, aristaNext)
            tipo = None

            #aristaActual < vecino indica que el vecino está por debajo en el orden de barrido
            if (aristaActual < aristaPrev) and (aristaActual < aristaNext):
                if determinante > 0:
                    tipo = TipoVertice.START
                else:
                    tipo = TipoVertice.SPLIT
            elif (aristaPrev < aristaActual) and (aristaNext < aristaActual):
                if determinante > 0:
                    tipo = TipoVertice.END
                else:
                    tipo = TipoVertice.MERGE
            else:
                tipo = TipoVertice.REGULAR

            clasificacionVertices[aristaActual] = tipo

        #Sincronizar clasificación en la lista doblemente ligada circular
        for nodo in self.dcel.nodosCircular:
            nodo.tipoVertice = clasificacionVertices.get(nodo.P)

        return clasificacionVertices

    def hacerMonotono(self) -> list[list['Point']]:
        clasificacion = self.clasificarVertices()

        #Guardar aristas originales del contorno antes de insertar diagonales
        #Se guardan las aristas exteriores antes del barrido para que al agregar diagonales internas en la DCEL no se pierda qué pared del borde sale o llega a cada vértice.
        aristaSalidaOriginal = {}
        aristaLlegadaOriginal = {}
        for arista in self.dcel.mediasAristas:
            if arista.trianguloPertenece == 0:
                aristaSalidaOriginal[arista.origenP] = arista
                aristaLlegadaOriginal[arista.next.origenP] = arista

        #Orden de mayor a menor y, en una fila
        verticesLista = sorted(self.dcel.verticesP)
        verticesOrdenados = ArrayQueue()
        for vertice in verticesLista:
            verticesOrdenados.enqueue(vertice)

        #Árbol Binario de Búsqueda
        bst = BST()
        helper = {}

        #Línea de barrido
        while not verticesOrdenados.is_empty():
            self.operaciones += 1
            v = verticesOrdenados.dequeue()
            tipo = clasificacion[v]

            mediaArSale = aristaSalidaOriginal[v]
            mediaArLlega = aristaLlegadaOriginal[v]

            #Casos por cada tipo de vértices
            if tipo == TipoVertice.START:
                bst.insertar(mediaArSale, v.y)
                helper[mediaArSale] = v

            elif tipo == TipoVertice.END:
                #Si el helper de la arista que termina es MERGE, se traza una diagonal
                if helper.get(mediaArLlega) and clasificacion.get(helper[mediaArLlega]) == TipoVertice.MERGE:
                    self.dcel.masDiagonal(v, helper[mediaArLlega])
                    self.diagonales.append((v, helper[mediaArLlega]))
                bst.eliminar(mediaArLlega)

            elif tipo == TipoVertice.SPLIT:
                #Busca arista inmediata a la izquierda
                aristaIzq = bst.buscarIzquierda(v.x, v.y)
                if aristaIzq is None or aristaIzq not in helper:
                    raise ErrorTriangulacion(f"No se encontró arista izquierda válida para el vértice SPLIT {v}.")
                self.dcel.masDiagonal(v, helper[aristaIzq])
                self.diagonales.append((v, helper[aristaIzq]))
                helper[aristaIzq] = v
                bst.insertar(mediaArSale, v.y)
                helper[mediaArSale] = v

            elif tipo == TipoVertice.MERGE:
                if helper.get(mediaArLlega) and clasificacion.get(helper[mediaArLlega]) == TipoVertice.MERGE:
                    self.dcel.masDiagonal(v, helper[mediaArLlega])
                    self.diagonales.append((v, helper[mediaArLlega]))
                bst.eliminar(mediaArLlega)

                aristaIzq = bst.buscarIzquierda(v.x, v.y)
                if aristaIzq is not None:
                    if helper.get(aristaIzq) and clasificacion.get(helper[aristaIzq]) == TipoVertice.MERGE:
                        self.dcel.masDiagonal(v, helper[aristaIzq])
                        self.diagonales.append((v, helper[aristaIzq]))
                    helper[aristaIzq] = v

            elif tipo == TipoVertice.REGULAR:
                # Si el interior del polígono queda a la derecha de v (arista llega desde arriba y sale hacia abajo)
                #Con vértices tipo REGULAR hay dos casos:
                #1. Si el polígono está a su derecha, reemplaza la pared activa en el BST
                #2. Si el polígono está a su izquierda, actualiza el helper de la pared izquierda
                if (mediaArLlega.origenP < v) and (v < mediaArSale.next.origenP):
                    if helper.get(mediaArLlega) and clasificacion.get(helper[mediaArLlega]) == TipoVertice.MERGE:
                        self.dcel.masDiagonal(v, helper[mediaArLlega])
                        self.diagonales.append((v, helper[mediaArLlega]))
                    bst.eliminar(mediaArLlega)
                    bst.insertar(mediaArSale, v.y)
                    helper[mediaArSale] = v
                else:
                    aristaIzq = bst.buscarIzquierda(v.x, v.y)
                    if aristaIzq is not None:
                        if helper.get(aristaIzq) and clasificacion.get(helper[aristaIzq]) == TipoVertice.MERGE:
                            self.dcel.masDiagonal(v, helper[aristaIzq])
                            self.diagonales.append((v, helper[aristaIzq]))
                        helper[aristaIzq] = v

        # etorna subpolígonos ya y-monótonos extraídos de la DCEL
        return self.dcel.extraerSubpoligonos()

    def triangularPoligonoMonotono(self, yMonotono: list['Point']):
        nSub = len(yMonotono)
        #Se necesitan 3 o más vértices para triangular
        if nSub < 3:
            return self.triangulos

        #Identificar vértice superior e inferior para separar cadenaIzquierda (recorrido antihorario)
        #Como el subpolígono va en sentido antihorario, avanzar del punto más alto (indiceSuperior) al más bajo (indiceInferior) marca toda la frontera izquierda.
        indiceSuperior = min(range(nSub), key=lambda idx: yMonotono[idx])
        indiceInferior = max(range(nSub), key=lambda idx: yMonotono[idx])

        cadenaIzquierda = set()
        actualIdx = indiceSuperior
        while actualIdx != indiceInferior:
            cadenaIzquierda.add(yMonotono[actualIdx])
            actualIdx = (actualIdx + 1) % nSub

        verticesMonotono = sorted(yMonotono)  #De mayor a menor y

        #Inicia la pila con los dos primeros vértices (los más altos)
        pilaVertices = [verticesMonotono[0], verticesMonotono[1]]

        for i in range(2, len(verticesMonotono) - 1):
            self.operaciones += 1
            verticeActual = verticesMonotono[i]
            verticeTope = pilaVertices[-1]

            #Caso 1: El vértice actual está en la cadena opuesta al último de la pila, se vacía la pila formando triángulos sucesivos
            if (verticeActual in cadenaIzquierda) != (verticeTope in cadenaIzquierda):
                while len(pilaVertices) > 1:
                    self.operaciones += 1
                    v1 = pilaVertices.pop()
                    v2 = pilaVertices[-1]
                    self.triangulos.append((verticeActual, v2, v1))
                pilaVertices.pop()
                pilaVertices.append(verticesMonotono[i - 1])
                pilaVertices.append(verticeActual)

            #Caso 2: Están en la misma cadena, uso de crossProduct para validar diagonales internas
            else:
                vUltimo = pilaVertices.pop()
                while len(pilaVertices) > 0:
                    self.operaciones += 1
                    vPrevio = pilaVertices[-1]
                    #Verificar con crossProduct si el giro es válido para formar un triángulo interno
                    determinante = Point.crossProduct(vPrevio, vUltimo, verticeActual)
                    #Giro válido según la cadena (izquierda: antihorario > 0; derecha: sentido horario < 0)
                    esGiroValido = (determinante > 0) if (verticeActual in cadenaIzquierda) else (determinante < 0)
                    if esGiroValido:
                        self.triangulos.append((vPrevio, vUltimo, verticeActual))
                        vUltimo = pilaVertices.pop()
                    else:
                        break
                pilaVertices.append(vUltimo)
                pilaVertices.append(verticeActual)

        #Conectar el último vértice (el más bajo) con los vértices restantes en la pila
        #El vértice inferior conecta con todos los vértices que quedaron sin cerrar en la pila
        verticeFinal = verticesMonotono[-1]
        while len(pilaVertices) > 1:
            self.operaciones += 1
            v1 = pilaVertices.pop()
            v2 = pilaVertices[-1]
            self.triangulos.append((verticeFinal, v2, v1))

        return self.triangulos  #Lista de tuplas de objetos Point que forman triángulos

    #Contrucción del árbol dual
    #Cada triángulo es un nodo (0, 1, ..., n-3). Si dos triángulos comparten exactamente 2 vértices (una diagonal), se unen con una arista.
    def construyeGraficaDual(self) -> dict:
        arbolDual = {}
        for a, trianguloA in enumerate(self.triangulos):
            arbolDual[a] = []
            for b, trianguloB in enumerate(self.triangulos):
                if a != b:
                    #Contar cuantos vértices comparten dos triángulos
                    verticesCompartidos = len(set(trianguloA).intersection(set(trianguloB)))
                    if verticesCompartidos == 2:
                        arbolDual[a].append(b)
        return arbolDual

    def asignaColores(self, arbolDual: dict) -> dict:
        for vertice in self.dcel.verticesP:
            vertice.color = None

        if not self.triangulos:
            return {}

        coloresDisponibles = {0, 1, 2}
        colaBFS = ArrayQueue()
        visitados = {0}
        colaBFS.enqueue(0)

        #Asignar los 3 colores al triángulo raíz del árbol dual
        for idxColor, vertice in enumerate(self.triangulos[0]):
            vertice.color = idxColor

        #Recorrido en anchura (BFS) con ArrayQueue para propagar la 3-coloración
        #Cada triángulo vecino comparte 2 vértices ya pintados con el triángulo anterior; al tercer vértice libre se le asigna el único color restante.
        while not colaBFS.is_empty():
            self.operaciones += 1
            trianguloActual = colaBFS.dequeue()
            for trianguloVecino in arbolDual.get(trianguloActual, []):
                if trianguloVecino not in visitados:
                    visitados.add(trianguloVecino)
                    triangulo = self.triangulos[trianguloVecino]
                    coloresVecinos = {v.color for v in triangulo if v.color is not None}
                    coloresLibres = coloresDisponibles - coloresVecinos
                    if not coloresLibres:
                        raise ErrorTriangulacion("No fue posible completar la 3-coloración válida del triángulo.")
                    colorNuevo = list(coloresLibres)[0]
                    for v in triangulo:
                        if v.color is None:
                            v.color = colorNuevo
                    colaBFS.enqueue(trianguloVecino)

        diccPoint = {vertice: vertice.color for vertice in self.dcel.verticesP}
        return diccPoint

    #Aplicación del teorema de Fisk, Agrupa los vértices por color {0, 1, 2} y elige el grupo con menor cantidad de vértices, garantizando siempre <= floor(n/3) cámaras.
    def seleccionarUbicacion(self, diccPoint: Optional[dict] = None) -> list['Point']:
        conteoColores = {0: 0, 1: 0, 2: 0}
        verticesPorColor = {0: [], 1: [], 2: []}

        listaVertices = list(diccPoint.keys()) if diccPoint is not None else self.dcel.verticesP

        for vertice in listaVertices:
            c = diccPoint[vertice] if diccPoint is not None else vertice.color
            if c in conteoColores:
                conteoColores[c] += 1
                verticesPorColor[c].append(vertice)

        ubicacionesCamaras = min(conteoColores, key=conteoColores.get)
        return verticesPorColor[ubicacionesCamaras]


# VALIDACIÓN Y FUNCIÓN PARA TRIANGULAR EL POLIGONO 
def _segmentosSeCruzan(p1: Point, p2: Point, q1: Point, q2: Point) -> bool:
    #Verifica si dos segmentos no adyacentes (p1, p2) y (q1, q2) se intersectan.
    #Uso de técnica de optimización de descarte por caja envolvente o también llamada Bounding Box Rejection
    if max(p1.x, p2.x) < min(q1.x, q2.x) or max(q1.x, q2.x) < min(p1.x, p2.x):
        return False
    if max(p1.y, p2.y) < min(q1.y, q2.y) or max(q1.y, q2.y) < min(p1.y, p2.y):
        return False

    #Prueba de orientación, dos segmentos se cruzan si los extremos de uno quedan en lados opuestos de la recta del otro (signos opuestos en crossProduct).
    d1 = Point.crossProduct(p1, p2, q1)
    d2 = Point.crossProduct(p1, p2, q2)
    d3 = Point.crossProduct(q1, q2, p1)
    d4 = Point.crossProduct(q1, q2, p2)

    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))


def validarPoligonoSimple(puntos: list['Point']):
    #Valida que no existan puntos duplicados, 3 colineales seguidos ni auto-intersecciones
    n = len(puntos)
    if n < 3:
        raise ErrorPoligonoInvalido("El polígono debe tener al menos 3 vértices.")

    #Verifica con un conjunto (set) que no haya coordenadas duplicadas
    coordenadasVistas = set()
    for p in puntos:
        clave = (round(p.x, 9), round(p.y, 9))
        if clave in coordenadasVistas:
            raise ErrorPoligonoInvalido(f"Se detectó un vértice duplicado en ({p.x}, {p.y}).")
        coordenadasVistas.add(clave)
    #Verifica que 3 vértices seguidos no formen una línea recta (det == 0)
    for i in range(n):
        pPrev = puntos[(i - 1) % n]
        pAct = puntos[i]
        pNext = puntos[(i + 1) % n]
        if abs(Point.crossProduct(pPrev, pAct, pNext)) < 1e-12:
            raise ErrorPoligonoInvalido(f"Vértices colineales consecutivos detectados alrededor de {pAct}.")
    #Compara pares de paredes no vecinas para asegurar polígono simple
    for i in range(n):
        a1 = puntos[i]
        a2 = puntos[(i + 1) % n]
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue  #Ignorar aristas adyacentes que comparten vértice
            b1 = puntos[j]
            b2 = puntos[(j + 1) % n]
            if _segmentosSeCruzan(a1, a2, b1, b2):
                raise ErrorPoligonoInvalido(f"El polígono no es simple: las aristas ({a1}-{a2}) y ({b1}-{b2}) se cruzan.")


#Función fuera de la clase que llame a triangular poligono.
def triangularPoligono(coordenadas: list[tuple[float, float]]) -> dict:
    """
    Función principal que recibe una lista de tuplas (x, y) o de objetos Point,
    construye las estructuras (DCEL, Plane Sweep, BST, Stack, Árbol Dual, ArrayQueue)
    y ejecuta todo el flujo del Problema de la Galería de Arte.
    """
    if not coordenadas or len(coordenadas) < 3:
        raise ErrorPoligonoInvalido("Debe proporcionar una lista con al menos 3 coordenadas (x, y).")
    #Convierte las tuplas (x, y) a objetos Point y valida el polígono
    Point.verticeID = 0
    puntos = []
    for item in coordenadas:
        if isinstance(item, Point):
            puntos.append(Point(item.x, item.y))
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            puntos.append(Point(item[0], item[1]))
        else:
            raise ErrorPoligonoInvalido(f"Formato de vértice inválido: {item}. Use tuplas (x, y).")

    validarPoligonoSimple(puntos)

    #Arma la DCEL y ejecuta Plane Sweep para eliminar vértices SPLIT/MERGE
    dcel = DCEL(puntos)
    triangulador = TrianguladorPoligono(dcel)

    subpoligonosMonotonos = triangulador.hacerMonotono()
    for subpoligono in subpoligonosMonotonos:
        triangulador.triangularPoligonoMonotono(subpoligono)

    #Conecta triángulos adyacentes, colorea vía BFS y elige cámaras
    arbolDual = triangulador.construyeGraficaDual()
    diccPoint = triangulador.asignaColores(arbolDual)
    camaras = triangulador.seleccionarUbicacion(diccPoint)

    #Comprueba n-2 triángulos y cota teórica <= floor(n/3)
    n = len(puntos)
    if len(triangulador.triangulos) != n - 2:
        raise ErrorTriangulacion(f"Invariante violado: se esperaban {n - 2} triángulos y se obtuvieron {len(triangulador.triangulos)}.")
    if len(camaras) > n // 3:
        raise ErrorTriangulacion(f"Cota de Fisk violada: se obtuvieron {len(camaras)} cámaras para n={n} (máximo {n // 3}).")

    return {
        "nVertices": n,
        "dcel": dcel,
        "triangulador": triangulador,
        "subpoligonosMonotonos": subpoligonosMonotonos,
        "diagonales": triangulador.diagonales,
        "triangulos": triangulador.triangulos,
        "arbolDual": arbolDual,
        "diccPoint": diccPoint,
        "camaras": camaras,
    }