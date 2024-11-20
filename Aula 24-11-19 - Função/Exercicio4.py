'''
Exercício 6 – Escreva um programa que recebe um número N e
escreve no terminal todos os números primos de 1 até N. Reutilize
a função eh_primo do exercício anterior.
'''

def verifica_primo(num):
    if num == 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

num = int(input("Digite um número: "))

for i in range(1, num + 1):
    if verifica_primo(i):
        print(i)