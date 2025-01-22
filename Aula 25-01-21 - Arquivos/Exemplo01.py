f = open('teste.txt', 'w+') # Abre o arquivo que eu quero manipular
# b em modo binário
# r em modo leitura
# w em modo escrita
# a em modo append
# w+ em modo leitura e escrita, cria o arquivo se não existir

conteudo = f.read() # Lê o conteúdo do arquivo

f.close() # Fecha o arquivo

print(conteudo)