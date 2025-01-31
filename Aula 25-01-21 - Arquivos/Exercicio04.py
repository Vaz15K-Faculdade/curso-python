with open('emails.txt', 'r') as file:
    for linha in file:
        if (linha.find('@') == -1 or linha.find('.') == -1):
            print(f'{linha.strip()} não é um email válido')