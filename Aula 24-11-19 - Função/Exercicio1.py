'''
Exercício 1 – Faça uma função chamada par_ou_impar que recebe
como argumento um número e escreve no terminal se o número é
par ou ímpar.
'''
def par_ou_impar(num):
    if num % 2 == 0:
        return True
    else:
        return False

num = int(input("Digite um número: "))

print("O numero é par") if par_ou_impar(num) else print("O número é impar")