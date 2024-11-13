lista = [12, 14, 8, 7, 21, 45, 1001]
lista_pares = []

for item in lista:
    if item % 2 == 0:
        print(f"{item} é par")
        lista_pares.append(item)
    else:
        print(f"{item} é ímpar")

print(f"Lista de pares: {lista_pares}")