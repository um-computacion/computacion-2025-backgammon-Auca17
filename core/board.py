class Board:
    def __init__(self):
        # El tablero tiene 24 puntos (triángulos)
        self.points = [None for _ in range(24)]
        # La barra central separa ambos lados
        self.bar = None
        # Lados del tablero
        self.left_side = self.points[:12]
        self.right_side = self.points[12:]

    def display(self):
        print("Backgammon Board:")
        print("Left Side:", self.left_side)
        print("Bar:", self.bar)
        print("Right Side:", self.right_side)