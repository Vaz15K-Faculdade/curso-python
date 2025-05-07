class Circulo():
    def __init__(self, raio):
        self.raio = raio

    def calcular_area(self):
        import math
        return round((2 * math.pi * self.raio**2), 2)

    def __str__(self):
        return f"Raio da circuferencia: {self.raio}\n"

class Retangulo():
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return round((self.base * self.altura), 2)

    def __str__(self):
        return f"Base do retangulo: {self.base}\n" \
                f"Altura do retangulo: {self.altura}\n"

class Triangulo():
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return round((self.base * self.altura) / 2, 2)

    def __str__(self):
        return f"Base do triangulo: {self.base}\n" \
                f"Altura do triangulo: {self.altura}\n"


t = Triangulo(10, 5)
r = Retangulo(10, 5)
c = Circulo(10)

print(t)
print(r)
print(c)

print(c.calcular_area())
print(r.calcular_area())
print(t.calcular_area())