with open('emails.txt', 'w') as file:
    email = []
    while True:
        email.append(input('Digite um email: '))
        if email == 'sair':
            break
        else :
            print(email)
            file.write(email[-1] + '\n')

"""
emails = []

while True:
    email = input("Digite um email ou sair para finalizar: ")
    if email == "sair":
        break
    emails.append(email)

with open("emails.txt", "w") as file:
    for i in emails:
        file.write(i + "\n")
"""