# Clases base: Point, TipoVertice, NodoVertice, MediaArista, DCEL

class TipoVertice:
    def __init__(self, tipo):
        self.tipo = tipo

class NodoVertice:
    def __init__(self, point, vertex_type):
        self.point = point
        self.vertex_type = vertex_type

class MediaArista:
    def __init__(self):
        self.origin = None         # Vértice de origen (NodoVertice)
        self.twin = None           # Su arista gemela (MediaArista)
        self.next = None           # Siguiente arista en el recorrido
        self.prev = None           # Arista anterior
        self.incident_face = None  # Cara a la que pertenece esta arista (Face)

class DCEL:
    def __init__(self):
        self.vertices = []
        self.half_edges = []
        self.faces = []