emails = []

with open('emails.txt', 'r') as file:
    for linha in file:
        emails.append(linha.strip())
        print(emails[-1])
        # strip() remove os espaços em branco no início e no final da string

# print(emails)