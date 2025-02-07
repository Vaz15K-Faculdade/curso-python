from docxtpl import DocxTemplate

# Carrega o docx template
doc = DocxTemplate("template1.docx") 

# substitui o "{{ minha_variavel }}" do documento de template
doc.render(
    {
        "minha_variavel": "Uma frase muito foda aqui!!"
    }
)

""" Mesma coisa que o de cima
contexto = {
        "minha_variavel": "Uma frase muito foda aqui!!"
    }

    doc.render(contexto)
"""

# Salva em um novo documento
doc.save("teste1.docx")