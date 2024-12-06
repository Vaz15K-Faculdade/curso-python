venda = []
lista_up = []
a = 0

while True:
    venda.append(float(input("Digite o valor da venda: ")))
    # Append adiciona um elemento ao fim lista

    if venda[-1] == -1:
        venda.pop(-1)
        break

venda.sort()
# Ordena a Lista de Forma Crescente

media = sum(venda) / len(venda)
# Sum faz soma e len faz contagem de elementos

for i in range(len(venda)):
    if venda[i] > media:
        a += 1
    if venda[i] > 1000:
        lista_up.append(venda[i])

print(f'A soma das vendas foi {sum(venda)}')
print(f'{a} vendas foram acima da média')
print(f'O maior valor da venda foi {max(venda)}')
# Max retorna o maior valor da lista
print(f'{lista_up}]')