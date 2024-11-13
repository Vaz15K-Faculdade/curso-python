'''
Faça um programa que mostre a multiplicação de um
número por ele mesmo no seguinte padrão: n x n = m, para cada
número de 0 a 100.

edit: permitir que o usuário escolha o intervalo de números
'''

numero_inicial = int(input("Digite o número inicial: "))
numero_final = int(input("Digite o número final: "))

for numero in range (numero_inicial, numero_final + 1):
    print(f"{numero} x {numero} = {numero * numero}")
    numero += 1