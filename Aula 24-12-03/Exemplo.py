lista_compras = ['leite', 'macarão', 'Carne', 'Ovos', 'Alfaces']

for i in range(0, len(lista_compras)):
    if (i >= 2) and (i <= 4):
        lista_compras[i] = input('Digite o novo item: ')

for i in range(0, len(lista_compras)):
    print(lista_compras[i])

if 'Carne' in lista_compras:
    print('Carne está na lista de compras')

if 'Carne' not in lista_compras:
    print('Carne não está na lista de compras')
