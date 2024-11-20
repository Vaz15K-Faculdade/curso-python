'''
Exercício 2 – Reescreva o programa de cálculo de IMC para que o
cálculo seja feito por uma função chamada calcula_imc. A função
deve receber os valores de altura e peso e retornar o IMC.

Exercício 3 – Reescreva o programa de cálculo de IMC para que a
classificação do IMC seja feita por uma função chamada classifica_imc.
A função recebe o valor do IMC e escreve no terminal a classificação
do IMC.

Exercício 4 – Reescreva o exercício 3, mas dessa vez a função
classifica_imc deve retornar a classificação do IMC como string.
'''

def calcula_imc (peso, altura):
    imc = peso / (altura ** 2)
    return imc

def classe_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc >= 18.5 and imc < 24.9:
        return "Peso normal"
    elif imc >= 25 and imc < 29.9:
        return "Sobrepeso"
    elif imc >= 30 and imc < 34.9:
        return "Obesidade grau 1"
    elif imc >= 35 and imc < 39.9:
        return "Obesidade grau 2"
    else:
        return "Obesidade grau 3"

peso = float(input("Digite o seu peso: "))
altura = float(input("Digite a sua altura: "))

imc = calcula_imc(peso, altura)

print(f"Seu IMC é {imc:.2f} e você está na categoria: {classe_imc(imc)}")