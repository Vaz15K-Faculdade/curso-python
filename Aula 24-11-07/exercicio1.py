'''
Exercício 3 - Faça um jogo de apostas com as seguintes
características:

1 - O usuário aposta em 2 números inteiros de 0 a 9.
2 - O programa seleciona 4 números de 0 a 9 aleatoriamente,
podendo haver números repetidos.
3 - Se um dos números apostados estiver entre os 4 selecionados,
o usúario é premiado com R$1000
4 - Se os dois números apostados estiver entre os 4 selecionados,
o usuário é premiado com R$2000

A saída do programa é o valor do prêmio
'''

import random

numero1 = int(input("Escolha o primeiro número (0 a 9): "))
numero2 = int(input("Escolha o segundo número (0 a 9): "))

num_1 = random.randint(0, 9)
num_2 = random.randint(0, 9)
num_3 = random.randint(0, 9)
num_4 = random.randint(0, 9)

if (numero1 == num_1 or numero1 == num_2 or numero1 == num_3 or numero1 == num_4) and (numero2 == num_1 or numero2 == num_2 or numero2 == num_3 or numero2 == num_4):
    print("Parabéns, você ganhou R$2000")
elif numero1 == num_1 or numero1 == num_2 or numero1 == num_3 or numero1 == num_4 or numero2 == num_1 or numero2 == num_2 or numero2 == num_3 or numero2 == num_4:
    print("Parabéns, você ganhou R$1000")
else:
    print("Que pena, você não ganhou nada")