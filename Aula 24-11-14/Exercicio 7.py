'''
Exercício 8 - Faça um programa que recebe do usúario as seguintes
informações:
Valor inicial do investimento (R$)
Aporte mensal (R$)
Taxa de juros do período
Quantidade de períodos
E então o programa deve calcular o valor futuro daquele
investimento e mostrar ao usúario.

edit: Modifique o exercício 8 para mostrar também o valor
total aportado pelo usúario e o valor ganho em juros.
'''

valor_inicial = float(input("Valor inicial do investimento (R$): "))
aporte_mensal = float(input("Aporte mensal (R$): "))
taxa_juros = float(input("Taxa de juros do período (%): ")) / 100
periodos = int(input("Quantidade de períodos: "))

valor_futuro = valor_inicial
total_aportado = valor_inicial

for i in range(periodos):
    valor_futuro = valor_futuro * (1 + taxa_juros) + aporte_mensal
    total_aportado += aporte_mensal

valor_juros = valor_futuro - total_aportado

print(f"Valor futuro: R${valor_futuro:.2f}")
print(f"Total aportado: R${total_aportado:.2f}")
print(f"Valor ganho em juros: R${valor_juros:.2f}")