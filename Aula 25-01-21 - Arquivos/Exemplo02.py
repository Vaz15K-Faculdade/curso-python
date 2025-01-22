with open('teste.txt', 'w+') as f:
    conteudo = f.read()
# o with é um gerenciador de contexto, ele abre e fecha o arquivo automaticamente

print(conteudo)