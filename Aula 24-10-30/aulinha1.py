nome = input("Informe seu nome: ")
idade = int(input("Informe a sua idade: "))

# Mesmo jeito de escrever
print("Bem vindo", end=" ")
print(nome, end=" ")
print("!!!")

print(f'Bem vindo: {nome}, {20 if (idade > 20) else 40} anos de idade !!!')

print("Bem vindo", nome, ",", idade, "anos de idade !!!")
# Mesmo jeito de escrever


if (idade > 18):
    print("Maior de Idade")
elif (idade >= 0 & idade < 18):
    print("Menor de Idade")
else:
    print("Você existe?")
