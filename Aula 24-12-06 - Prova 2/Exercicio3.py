def soma():
    n1 = float(input("Digite o primeiro numero: "))
    n2 = float(input("Digite o segundo numero: "))

    print(f"Resultado {n1 + n2}")

def subtracao():
    n1 = float(input("Digite o primeiro numero: "))
    n2 = float(input("Digite o segundo numero: "))

    print(f"Resultado {n1 - n2}")

def multiplicacao():
    n1 = float(input("Digite o primeiro numero: "))
    n2 = float(input("Digite o segundo numero: "))

    print(f"Resultado {n1 * n2}")

def divisao():
    n1 = float(input("Digite o primeiro numero: "))
    n2 = float(input("Digite o segundo numero: "))

    if n2 == 0:
        print("Erro: Divisão por zero não permitida.")
    else:
        print(f"Resultado {n1 / n2}")

while True:
    print("Escolha uma operação:\n"
        "1 - Soma\n"
        "2 - Subtração\n"
        "3 - Multiplicação\n"
        "4 - Divisão\n"
        "0 - Sair")
    opcao = int(input("Opção: "))

    if opcao == 0:
        print("Saindo do programa.")
        break

    if opcao < 1 or opcao > 4:
        print("Opção Invalida")
        continue

    if opcao == 4:
        divisao()
    elif opcao == 3:
        multiplicacao()
    elif opcao == 2:
        subtracao()
    else:
        soma()