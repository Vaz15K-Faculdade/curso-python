'''
Faça um programa que mostre do número 100 ao 0
usando while e outra versão usando for

edit: permitir que o usuário escolha o número inicial e final
'''
numero_inicial = int(input("Digite o número inicial: "))
numero_final = int(input("Digite o número final: "))

numero = numero_inicial

for numero in range(numero_inicial, numero_final - 1, -1):
    print(numero)

while numero >= numero_final:
    print(numero)
    numero += -1
