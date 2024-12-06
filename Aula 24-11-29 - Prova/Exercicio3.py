def validar_idades(lista_idades):
    a = 0
    idades_validas = []

    for idade in lista_idades:
        if idade < 0 or idade > 120:
            a += 1
        else:
            idades_validas.append(idade)
    
    print(f'A media das idades é {sum(idades_validas) / len(idades_validas)}')
    print(f'{a} idades inválidas')
    return idades_validas

lista_idades = []

while True:
    lista_idades.append(int(input("Digite a idade: ")))

    if lista_idades[-1] == -1:
        lista_idades.pop(-1)
        break

lista_valores = validar_idades(lista_idades)

print(f'{lista_valores}')