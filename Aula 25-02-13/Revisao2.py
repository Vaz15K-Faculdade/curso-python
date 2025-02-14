lista = []
lista_tupula_lista = []
dicionario_lista = {}
lista_dicionario_lista = []

qtd = int(input("Infome quantos alunos deseja cadastrar: "))

for k in range(qtd):
    notas= []
    
    nome = input("Infome o nome do aluno: ")
    for i in range(3):
        notas.append(input(f"Informe a nota {i+1}: "))

    lista.append(nome)
    lista.extend(notas)

    lista_tupula_lista.append((nome, notas))

    dicionario_lista[nome] = notas

    lista_dicionario_lista.append({"nome": nome, "notas": notas})

print(lista)
print(lista_tupula_lista)
print(dicionario_lista)
print(lista_dicionario_lista)

print("\nDados da lista simples:")
for i in range(0, len(lista), 4):
    print(f"Aluno: {lista[i]} - Notas: {lista[i+1]}, {lista[i+2]}, {lista[i+3]}")

print("\nDados da lista de tuplas:")
for nome, notas in lista_tupula_lista:
    print(f"Aluno: {nome} - Notas: {notas[0]}, {notas[1]}, {notas[2]}")

print("\nDados do dicionário:")
for nome, notas in dicionario_lista.items():
    print(f"Aluno: {nome} - Notas: {notas[0]}, {notas[1]}, {notas[2]}")

print("\nDados do lista de dicionário:")
for aluno in lista_dicionario_lista:
    print(f"Aluno: {aluno['nome']} - Notas: {aluno['notas'][0]}, {aluno['notas'][1]}, {aluno['notas'][2]}")
