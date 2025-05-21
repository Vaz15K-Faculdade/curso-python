class Fracao():
    def __init__(self, numerador, denominador):
        assert denominador != 0, "Denominador não pode ser zero"
        self.__numerador = numerador
        self.__denominador = denominador

    def getDenominador(self):
        return self.__denominador

    def getNumerador(self):
        return self.__numerador

    def setNumerador(self, numerador):
        self.__numerador = numerador

    def setDenominador(self, numerador):
        assert numerador != 0, "Numerador não pode ser 0"
        self.__denominador = numerador

    def __repr__(self):
        return f"Fração({self.__numerador}, {self.__denominador})"

f1 = Fracao(10, 2)
f2 = Fracao(25, 3)
f3 = Fracao(30, 1)

f3.__denominador = 0
# f3._Fracao__denominador = 0
# print(f3.__denominador)

print(f1)
print(f2)
print(f3)
