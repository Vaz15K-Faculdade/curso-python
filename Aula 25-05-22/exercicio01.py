import math

class Forma():
    def __init__(self):
        pass

    def area(self):
        return "Forma sem area"

class Quadrado(Forma):
    def __init__(self, lado):
        super().__init__()
        self.lado = lado

    def area(self):
        return self.lado ** 2

class Circulo(Forma):
    def __init__(self, raio):
        super().__init__()
        self.raio = raio

    def area(self):
        return math.pi * self.raio**2

formas = [Quadrado(5), Circulo(3)]
for forma in formas:
    print(f"A área da {forma.__class__.__name__} é: {forma.area():.2f}")