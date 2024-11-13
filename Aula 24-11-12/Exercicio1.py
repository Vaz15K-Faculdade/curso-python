from random import randint

numero = randint(0, 100)

palpite = int(input("Adivinhe um numero de 0 a 100: "))
tentativas = 1

while palpite != numero:
    print("Errou!")
    palpite = int(input("Tente novamente: "))
    tentativas += 1

print(f"Parabens, voce acertou! O número era {numero}")
print(f"Você acertou em {tentativas} tentativas")