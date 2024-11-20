'''
Exercício 5 – Escreva um programa que recebe um número N e
escreve no terminal se o número é primo ou não. Crie uma função
chamada eh_primo para fazer essa verificação.
'''
def verifica_primo(num):
    if num == 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

num = int(input("Digite um número: "))
if verifica_primo(num):
    print("O número é primo.")
else:
    print("O número não é primo.")
