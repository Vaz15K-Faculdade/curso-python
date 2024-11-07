''' teste 1
nota1 = float(input("Infome sua nota 1: "))
nota2 = float(input("Infome sua nota 2: "))
nota3 = float(input("Infome sua nota 3: "))

notas = nota1 + nota2 + nota3

print(f"Sua media é: {notas/3}")
'''

for i in range(3):
    nota = float(input(f"Informe sua Nota {i + 1}: "))
    if (i==0):
        soma = 0
    soma = soma + nota

media = soma / (i+1)

print(f"Suas media é: {media}")