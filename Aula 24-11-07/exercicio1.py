import random

numero1 = int(input("Escolha o primeiro número (0 a 9): "))
numero2 = int(input("Escolha o segundo número (0 a 9): "))

numeros_aleatorios = [random.randint(0, 9) for _ in range(4)]

if numero1 in numeros_aleatorios and numero2 in numeros_aleatorios:
    print(f"Parabens, você ganhou R$2000")
elif numero1 in numeros_aleatorios or numero2 in numeros_aleatorios:
    print(f"Parabens, você ganhou R$1000")
else:
    print(f"Que pena, você não ganhou nada")