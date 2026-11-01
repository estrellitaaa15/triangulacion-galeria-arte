# Clases Lista Doblemente Ligada DCEL (Vertex), (HalfEdge), Face

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.incident_edge = None  # Apunta a una HalfEdge que sale de aquí

class MediaArista:
    def __init__(self):
        self.origin = None         # Vértice de origen (Vertex)
        self.twin = None           # Su arista gemela (HalfEdge)
        self.next = None           # Siguiente arista en el recorrido
        self.prev = None           # Arista anterior
        self.incident_face = None  # Cara a la que pertenece esta arista (Face)

class Face:
    def __init__(self):
        self.outer_component = None # Apunta a una de las aristas del borde del polígono