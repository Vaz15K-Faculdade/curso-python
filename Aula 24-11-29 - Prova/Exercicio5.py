def analise_nota(lista_notas):
    abaixo = 0

    for i in range(len(lista_notas)):
        if lista_notas[i] < 7:
            abaixo += 1
    
    media = sum(lista_notas) / len(lista_notas)

    print(f'Notas abaixo de 7: {abaixo}')
    
    if media < 7:
        print(f'Conceito D')
    elif media < 8:
        print(f'Conceito C')
    elif media < 9:
        print(f'Conceito B')
    else:
        print(f'Conceito A')

lista_notas = []

while True:
    i = 0
    lista_notas.append(float(input(f"Digite a nota {i + 1}: ")))
    i += 1

    if lista_notas[-1] == -1:
        lista_notas.pop(-1)
        break

analise_nota(lista_notas)