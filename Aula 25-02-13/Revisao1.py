lista = []

def par_impar(numero):
    return "par" if numero % 2 == 0 else "impar"

for i in range(10):
    numero = int(input(f"Informe o numero {i+1}: "))
    lista.append(numero)

media = sum(lista) / len(lista)

for numero in lista:
    print(f"Numero {numero} é {par_impar(numero)}")
    
    if numero < 0:
        print(f"Numero {numero} é negativo")
    
    if numero > media:
        print(f"Numero {numero} está acima da média ({media}) \n")