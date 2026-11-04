# Clases base: Point, TipoVertice, NodoVertice, MediaArista, DCEL
#Librerias
from enum import Enum, unique

#Clases
class Point:
    def __init__(self, x, y, id_punto):
        self.x = x
        self.y = y
        self.id = id_punto

    def __repr__(self):
        return f"V{self.id}({self.x}, {self.y})"

def cross_product(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def is_point_in_triangle(pt, v1, v2, v3):

    d1 = cross_product(v1, v2, pt)
    d2 = cross_product(v2, v3, pt)
    d3 = cross_product(v3, v1, pt)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)


class TipoVertice(Enum):
  START = 1
  END = 2
  SPLIT = 3
  MERGE = 4
  REGULAR = 5

class NodoVertice:
    __slots__ = 'P', 'prev', 'next', 'tipoVertice'   # tipoVertice agregado

    def __init__(self, P, prev=None, next=None):
        self.P = P
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
        raise NotImplementedError("masDiagonal: falta reconectar punteros")