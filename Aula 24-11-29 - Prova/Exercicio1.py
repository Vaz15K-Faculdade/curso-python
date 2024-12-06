def calcular_media(val1, val2, val3, val4):
    media = (val1 + val2 + val3 + val4) / 4
    return format(media, '.2f')

valores = []
i = 0

while i < 6:
    valores.append(float(input(f"Digite o resultado da prova {i + 1}: ")))
    i += 1

valores.sort()

print(f"A media do atleta é {calcular_media(valores[1], valores[2], valores[3], valores[4])}")