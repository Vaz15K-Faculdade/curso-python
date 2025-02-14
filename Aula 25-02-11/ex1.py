numeros = []

def somar(numero):
    total = 0
    for i in numero:
        total += i
    return total

def media(numero):
    total = 0
    for i in numero:
        total += i
    return (total / len(numero))

def maior(numero):
    for count, i in enumerate(numero):
        if count == 0:
            maior_numero = i
        elif i > maior_numero:
            maior_numero = i
    return maior_numero

def menor(numero):
    for count, i in enumerate(numero):
        if count == 0:
            menor_numero = i
        elif i < menor_numero:
            menor_numero = i
    return menor_numero

for j in range(10):
    numeros.append (int(input(f"Informe o numero {j+1}: ")))

print(f"Soma = {somar(numeros)} \n"
      f"Media = {media(numeros)} \n"
      f"Maior = {maior(numeros)} \n"
      f"Menor = {menor(numeros)} \n")