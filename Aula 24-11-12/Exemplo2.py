from random import randint

numero = randint(0, 10)

palpite = int(input("Digite um número: "))

while palpite != numero:
    print("Errou!")
    palpites = int(input("Tente novamente: "))

print(f"Parabens, voce acertou! O número era {numero}")