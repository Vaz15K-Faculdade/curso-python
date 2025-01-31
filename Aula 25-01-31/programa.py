import json
from datetime import date

# Carrega o arquivo de produtos e cria a estrutura 'produtos'
#-------------------------------------------------------------------------------
with open('produtos.json', 'r') as arquivo_produtos:
    produtos = json.load(arquivo_produtos)

# Carrega o arquivo de vendas do e cria a estrutura 'vendas' (se o arquivo existir)
#-------------------------------------------------------------------------------
try:
    nome_arquivo_vendas = 'vendas' + date.today().isoformat() + '.json'
    with open(nome_arquivo_vendas, 'r') as arquivo_vendas:
        vendas = json.load(arquivo_vendas)
except:
    # Caso o arquivo não exista, iniciar uma estrutura em branco
    vendas = []


# Função para mostrar o recibo formatado
#-------------------------------------------------------------------------------
def mostrar_recibo(lista_vendas):
    """
    Essa função mostra no terminal o recibo formatado. Para isso ela deve receber 
    uma lista de compras, em que cada elemento é uma tupla (ou lista) com os elementos quantidade, descrição e preço.

    Exemplo de entrada:
    ```
    [(2, 'Coca-Cola 2L', 19.00),
    (0.5, 'Pao Frances KG', 9.50),
    (0.1, 'Queijo Prato KG', 6.90),
    (0.05, 'Tomate Seco KG', 5.00),
    (1, 'Rucula Baby Un.', 11.30),
    (4, 'Chocolate Snickers', 21.40)]
    ```

    Exemplo de saída:

    ```txt
       2 - Coca-Cola 2L        R$ 19.0
     0.5 - Pao Frances KG      R$  9.5
     0.1 - Queijo Prato KG     R$  6.9
    0.05 - Tomate Seco KG      R$  5.0
       1 - Rucula Baby Un.     R$ 11.3
       4 - Chocolate Snickers  R$ 21.4
    
    Total                      R$ 73.1
    ```

    """
    
    maxDigitosQnt = max(len(str(round(venda[0], 3))) for venda in lista_vendas)   
    maxDigitosDescricao = max(len(venda[1]) for venda in lista_vendas) 
    maxDigitosPreco = max(len(str(round(venda[2], 2))) for venda in lista_vendas)   

    total = 0

    for venda in lista_vendas:
        qnt = str(round(venda[0], 3))
        descricao = venda[1]
        preco = str(round(venda[2], 2))
        total += venda[2]

        espacoQnt = ' ' * (maxDigitosQnt - len(qnt))
        espacoDescricao = ' ' * (maxDigitosDescricao - len(descricao))
        espacoPreco = ' ' * (maxDigitosPreco - len(preco))

        print(f'{espacoQnt}{qnt} - {descricao}{espacoDescricao}  R$ {espacoPreco}{preco}')

    total = str(round(total, 2))
    espaco = ' ' * (maxDigitosQnt + maxDigitosDescricao)
    espacoPreco = ' ' * (maxDigitosPreco - len(total))
    print(f'\nTotal{espaco}R$ {espacoPreco}{total}')


# Efetuar venda
#-------------------------------------------------------------------------------
def efetuar_venda():
    vendas_local = []
    
    while True:
        codico = input('Digite o código do produto: ')
        if codico == "":
            mostrar_recibo(vendas_local)
            vendas.append(vendas_local)
            salvar_vendas()
            break
        elif codico not in produtos:
            print(f'Produto {codico} não encontrado')
            continue

        quantidade = float(input('Digite a quantidade: '))
        if quantidade <= 0:
            print('Quantidade inválida')
            continue

        descricao = produtos[codico]["nome"]
        preco = produtos[codico]["preco"]
        total = quantidade * float(preco)

        vendas_local.append([quantidade, descricao, total])

# Balancete
#-------------------------------------------------------------------------------
def balancete():
    total = 0
    for venda in vendas:
        for item in venda:
            total += item[2]
    print(f"Total de vendas: R$ {total:.2f}")

# Salvar arquivo de vendas
#-------------------------------------------------------------------------------
def salvar_vendas():
    nome_arquivo_vendas = 'vendas' + date.today().isoformat() + '.json'

    with open(nome_arquivo_vendas, 'w') as arquivo_vendas:
        json.dump(vendas, arquivo_vendas)

# Menu
#-------------------------------------------------------------------------------
def menu():
    while True:
        print('1 - Efetuar Venda')
        print('2 - Balancete')
        print('0 - Sair')
        
        opc = input('Digite a opção: ')

        if opc == '1':
            # Efetuar venda
            efetuar_venda()
        elif opc == '2': 
            # Balancete
            balancete()
        elif opc == '0':
            # Salvar vendas e sair
            salvar_vendas()
            break
        else:
            # Opção inválida
            print(f'Opção {opc} é inválida')

        

# Chama a função menu
#-------------------------------------------------------------------------------
menu()

