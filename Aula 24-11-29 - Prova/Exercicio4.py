def gerar_sequencia_personalizada(inicio, fim, regra):
    for i in range(inicio, fim + 1):
        if regra == 1:
            lista_numeros.append(i * 2)
        elif regra == 2:
            lista_numeros.append(i ** 2)
        elif regra == 3:
            lista_numeros.append(i + 10)
        elif regra == 4:
            lista_numeros.append(i - 5)
        else:
            print("Regra inválida")
            break

    print(lista_numeros)

lista_numeros = []

inicio = int(input("Digite o inicio da sequencia: "))
fim = int(input("Digite o fim da sequencia: "))
regra = int(input("Digite a regra da sequencia: \n"
                  "1 - Drobrar o valor \n"
                  "2 - Elevar ao quadrado \n"
                  "3 - somar 10 \n"
                  "4 - Subtrair 5\n"))

gerar_sequencia_personalizada(inicio, fim, regra)
