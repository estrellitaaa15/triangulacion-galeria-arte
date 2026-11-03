class Point:
    def __init__(self, x, y, id_punto):
        self.x = x
        self.y = y
        self.id = id_punto

    def __repr__(self):
        return f"V{self.id}({self.x}, {self.y})"

def cross_product(p1, p2, p3):
    # Determinante de matriz 3x3: > 0 giro a la izquierda (convexo), < 0 giro a la derecha (reflejo)
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
