'''
Fazer um programa que veja se um numero é primo ou nao, o usuario 
deve digitar um intervalo de numero e o programa  devera dizer quais sao primos.
'''

inicio = int(input("Digite o inicio do intervalo: "))
fim = int(input("Digite o fim do intervalo: "))

for i in range(inicio, fim + 1):
    if i > 1:
        primo = True
        for j in range(2, i):
            if i % j == 0:
                primo = False
                break
        if primo:
            print(i)
