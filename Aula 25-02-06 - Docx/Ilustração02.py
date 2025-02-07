from docxtpl import DocxTemplate

# Carrega o docx template
doc = DocxTemplate("template1.docx") 

carros = [
    ["Placa", "Marca", "Modelo", "Cor"],
    ["AVX-0102", "Fiat", "Toro", "Branco"],
    ["TRF-2398", "Nissan", "Leaf", "Prata"],
    ["RWD-3891", "Honda", "City", "Preto"]
]

contexto = {
    "carros": carros
}

doc.render(contexto)

# Salva em um novo documento
doc.save("teste1.docx")