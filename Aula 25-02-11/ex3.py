numero = int(input("Digite um numero: "))

acabou = False

while acabou == False:
    resto = (numero) % 10
    numero = int(numero/10)
    print(resto)
    if numero <= 0:
        acabou = True