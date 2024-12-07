def gerar_tabuada(numero, inicio, fim):
    for i in range(inicio, fim + 1):
        print(f"{numero} x {i} = {numero * i}")

while True:
    numero = int(input("Digite um numero pra a tabuada: "))
    inicio = int(input("Digite o numero inicial do intervalo: "))
    fim = int(input("Digite o numero final do intervalo: "))
    
    gerar_tabuada(numero, inicio, fim)

    opcao = input("Deseja continuar? (1 - Sim / 2 - Nao) ")
    if opcao == "2":
        print("Saindo do programa.")
        break