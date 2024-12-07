def contar_pares(inicio, fim):
    pares = 0
    
    for i in range(inicio, fim + 1):
        if i % 2 == 0:
            pares += 1
    return pares

def contar_impares(inicio, fim):
    impares = 0
    
    for i in range(inicio, fim + 1):
        if i % 2 != 0:
            impares += 1
    return impares

while True:
    inicio = int(input("Digite o inicio do intervalo: "))
    fim = int(input("Digite o fim do intervalo: "))
    
    if inicio >= fim:
        print("Intervalo invalido.")
    
    print(f"Quantidade de pares: {contar_pares(inicio, fim)}")
    print(f"Quantidade de impares: {contar_impares(inicio, fim)}")

    opcao = input("Deseja continuar? (1 - Sim / 2 - Nao) ")
    
    if opcao == "2":
        print("Saindo do programa.")
        break