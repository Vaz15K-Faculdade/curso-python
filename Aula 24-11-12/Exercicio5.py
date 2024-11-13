'''
Faça um programa que mostra na tela o seguinte
padrão, para qualquer número inteiro positivo n que o usúario
digitar:
0
01
012
0123
01234
'''

numero = int(input("Digite um número inteiro positivo: "))

for i in range (0, numero +1):
    for j in range (0, i + 1):
        print(j, end="")
    print()