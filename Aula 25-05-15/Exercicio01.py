# Exercício 1
# Crie uma classe Estudante com os seguintes atributos:
# - nome
# - turma 
# - notas: list[float]
# *** Todos os atributos devem ser privados ***
# 
# E com métodos:
# - adicionar_nota() - Validar a nota (0, 10)
# - media() 
# - get/set Nome
# - get/set Turma
# - get Notas
#

class Estudante():
    def __init__(self, nome, turma, notas: list[float] = []):
        self.__nome = nome
        self.__turma = turma
        self.__notas = notas
    
    def adicionar_nota(self, nota):
        assert nota > 0 or nota < 10, "Nota não está entre 0 e 10"
        self.__notas.append(nota)
    
    def media(self):
        assert self.__notas == [], "Lista vazia"
        soma = 0
        for i, nota in enumerate(self.__notas, 0):
            soma += nota
        
        print(f"A media é {soma / i}")
        return soma / i
    
    def getNome(self):
        return self.__nome
    
    def setNome(self, nome):
        self.__nome = nome
    
    def getTurma(self):
        return self.__turma
    
    def setTurma(self, turma):
        self.__turma = turma
    
    def getNotas(self):
        return self.__notas

    def __repr__(self):
        return (f"Estudante({self.__nome}, {self.__turma}, {self.__notas})")

e1 = Estudante("Lucas", "3A")
e2 = Estudante("Ana", "3B")

e1.adicionar_nota(10)
e1.adicionar_nota(8)
e1.adicionar_nota(9)
e1.adicionar_nota(7)

e2.adicionar_nota(10)
e2.adicionar_nota(8)
e2.adicionar_nota(9)
e2.adicionar_nota(7)

print(e1)
print(e2)
