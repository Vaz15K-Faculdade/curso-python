'''
Exercício 4 - Faça um conversor de unidades que permite ao
usuário converter valores no sistema metrico para o sistema
imperial.
Para isso seu programa deve receber qual o tipo de conversao e
logo em seguida receber tambem o valor que sera convertido.

”distancia”: m para pes
”velocidade”: km/h para milhas por hora
”massa”: kg para lbs
”volume”: litros para floz (onças líquidas)

No final mostre o valor convertido juntamente com a unidade de
medida: Por exemplo: ”23.7 lbs”
'''

print("Qual o tipo de conversão?")
tipo = input("1- Distância\n2- Velocidade\n3- Massa\n4- Volume\n")

if tipo == "1":
    valor = float(input("Digite o valor em metros: "))
    print(f"{valor * 3.28084} pés")
elif tipo == "2":
    valor = float(input("Digite o valor em km/h: "))
    print(f"{valor * 0.621371} milhas por hora")
elif tipo == "3":
    valor = float(input("Digite o valor em kg: "))
    print(f"{valor * 2.20462} lbs")
elif tipo == "4":
    valor = float(input("Digite o valor em litros: "))
    print(f"{valor * 33.814} fl oz")