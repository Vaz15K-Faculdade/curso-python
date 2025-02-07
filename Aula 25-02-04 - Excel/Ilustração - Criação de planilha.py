from openpyxl import Workbook

# Cria uma planilhas limpa
arquivo_excel = Workbook()

# seleciona a planilha ativa
# planilha = arquivo_excel.active

# Muda o nome da planilha
# planilha.title = "Dados"

# Cria uma nova aba dados dentro do arquivo
arquivo_excel.create_sheet('dados')

# Seleciona a Planilha dados
planilha = arquivo_excel['dados']

# Altera a celual 1,1 (A1) para o valor 'Teste!'
planilha.cell(1,1).value = 'Teste!'

# Salva
arquivo_excel.save('cadastro2.xlsx')