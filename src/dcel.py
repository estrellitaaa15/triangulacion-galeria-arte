# Clases base: Point, TipoVertice, NodoVertice, MediaArista, DCEL
#Librerias
from enum import Enum, unique

#Clases
class Point:
  verticeID = 0
  def __init__(self, x: float, y: float):
    Point.verticeID += 1
    self.idVertice = PointverticeID
    self.color = None
    self.x = float(x)
    self.y = float(y)

  def __lt__(self, P): #P son los objetos tipo Point
    if self.y == P.y:
      return self.x < P.x
    return self.y > P.y

  @staticmethod #Permite ejecutar el método directamente desde la clase sin necesidad de instanciar un objeto
  def crossProduct(P1, P2, P3):
    return (P2.x - P1.x) * (P3.y - P1.y) - (P2.y - P1.y) * (P3.x - P1.x)
    #Det positiva: giro izq
    #Det negativa: giro der
    #Det 0: recta

class TipoVertice(Enum):
  START = 1
  END = 2
  SPLIT = 3
  MERGE = 4
  REGULAR = 5

class NodoVertice:
  __slots__ = 'P', 'prev', 'next'
  def __init__(self, P, prev, next):
    self.P = P #Objeto Point
    self.tipoVertice = None
    self.prev = prev
    self.next = next

class MediaArista:
  __slots__ = 'origenP', 'twin', 'next', 'prev', 'trianguloPertenece'
  def __init__(self, origenP):
    self.origenP = origenP
    self.trianguloPertenece = None
    self.twin = None
    self.next = None
    self.prev = None
    #next -> siguiente media arista
    #prev -> media arista anterior
    
class DCEL:
  def __init__(self, verticesP: list['Point'], mediasAristas: list['MediaArista'], caras: list):
    self.verticesP = verticesP
    self.mediasAristas = mediasAristas
    self.caras = caras
  def masDiagonal(self, P1, P2):
    #Arista dirigida de A -> B y de B -> A
    diagonalAB = MediaArista(P1)
    diagonalBA = MediaArista(P2)
    #Uso de twin para relacionarlas
    diagonalAB.twin = diagonalBA
    diagonalBA.twin = diagonalAB

    aristasDeP1 = None
    aristasDeP2 = None

    for arista in self.mediasAristas:
        pass   