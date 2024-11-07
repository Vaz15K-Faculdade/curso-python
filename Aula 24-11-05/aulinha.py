idade = float(input("Digite a sua idade: "))

if (idade > 65):
    print("Oba \n Ja pode se aposentar")
elif idade == 65:
    print("ja entrou em processo de aposentadoria")
else:
    print("Ainda nao pode se aposentar :(")

print(f"Sua idade é {idade}")