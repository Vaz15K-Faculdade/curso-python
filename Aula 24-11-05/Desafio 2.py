peso = float(input("Informe seu peso: "))
altura = float(input("Informe a sua altura: "))

imc = (peso/(altura)**2)

if (imc >= 15 and imc <= 18.5):
    print(f"Abaixo do peso, IMC={round(imc,2)}")
elif (imc > 18.5 and imc < 25):
    print(f"Peso normal, IMC={round(imc,2)}")
elif (imc >= 25 and imc < 30):
    print(f"Acima do peso, IMC={round(imc,2)}")
elif (imc >= 30 and imc < 40):
    print(f"Obsidade grau I, IMC={round(imc,2)}")
elif (imc >= 40):
    print(f"Obsidade grau II, IMC={round(imc,2)}")
