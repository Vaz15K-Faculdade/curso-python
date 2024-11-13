'''
Faça um programa que recebe um número inteiro
positivo n do usuário e calcule a soma de 0 até n. Por exemplo:
(0 + 1 + 2 + 3 + ... + n).
'''

numero = int(input("Digite um número inteiro positivo: "))

soma = 0
for i in range (0, numero + 1):
    soma += i

print(f"A soma de 0 até {numero} é {soma}")