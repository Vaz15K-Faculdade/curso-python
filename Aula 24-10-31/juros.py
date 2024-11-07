v = float(input("Informe o valor inicial: "))
juros = float(input("Informe a Taxa de Juros: "))
t = int(input("Informe o tempo: "))

print(f"Seu retorno de investimento: {round((v * (1 + (juros/100))**t),2)}")
