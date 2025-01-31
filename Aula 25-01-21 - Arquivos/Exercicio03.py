dados_uso = []

with open('relatorio.txt', 'r') as rel:
    for linha in rel:
        dados_uso.append(linha.strip())

for dado in dados_uso:
    n, u = dado.split('=')
    uso = float(u) / 1048576
    print(f'{n} = {uso:.2f} MiB')
