while True:
    print('1 - Cadastrar CEP e rua')
    print('2 - Consultar rua pelo CEP')
    print('3 - Sair')

    opcao = input('Digite a opção desejada: ')

    if opcao == '1':
        cadastrar_cep(dicionario)
        dicionario[cep] = rua
    elif opcao == '2':
        cep = input('Digite o CEP: ')
        rua = buscar_cep(dicionario, cep)