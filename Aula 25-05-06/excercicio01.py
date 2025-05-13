class Pessoa():
    def __init__(self, nome, idade, endereco, cpf, sexo):
        self.nome = nome
        self.idade = idade
        self.endereco = endereco
        self.cpf = cpf
        self.sexo = sexo

    def __str__(self):
        return self.nome

    def resumo(self):
        print(f"Nome {self.nome}")
        print(f"Idade {self.idade}")
        print(f"Endereco {self.endereco}")
        print(f"CPF {self.cpf}")
        print(f"Sexo {self.sexo}")

class Pai(Pessoa):
    filhos = []
    esposa = []

    def __init__(self, nome, idade, endereco, cpf, sexo):
        super().__init__(nome, idade, endereco, cpf, sexo)

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def adicionar_esposa(self, esposa):
        self.esposa.append(esposa)

    def resumo(self):
        super().resumo()
        filhos_nomes = [str(filho) for filho in self.filhos]
        esposas_nomes = [str(esposa) for esposa in self.esposa]
        print(f"Filhos: {filhos_nomes}")
        print(f"Esposa: {esposas_nomes}")

class Mae(Pessoa):
    filhos = []
    marido = []

    def __init__(self, nome, idade, endereco, cpf, sexo):
        super().__init__(nome, idade, endereco, cpf, sexo)

    def adicionar_filho(self, filho):
        self.filhos.append(filho)

    def adicionar_marido(self, marido):
        self.marido.append(marido)

    def resumo(self):
        super().resumo()
        filhos_nomes = [str(filho) for filho in self.filhos]
        maridos_nomes = [str(marido) for marido in self.marido]
        print(f"Filhos: {filhos_nomes}")
        print(f"Marido: {maridos_nomes}")
        print()

class Filho(Pessoa):
    def __init__(self, nome, idade, endereco, cpf, sexo):
        super().__init__(nome, idade, endereco, cpf, sexo)
        self.pai = None
        self.mae = None

    def adicionar_pai(self, pai):
        self.pai = pai

    def adicionar_mae(self, mae):
        self.mae = mae

    def resumo(self):
        super().resumo()
        print(f"Pai {self.pai}")
        print(f"Mãe {self.mae}")


pai = Pai("João", 40, "Rua A", "12345678900", "Masculino")
amante = Pai("Carlos", 45, "Rua C", "98765432100", "Masculino")
mae = Mae("Maria", 38, "Rua B", "98765432100", "Feminino")
filho1 = Filho("Pedro", 10, "Rua A", "11122233344", "Masculino")
filho2 = Filho("Ana", 8, "Rua A", "55566677788", "Feminino")

pai.adicionar_filho(filho1)
pai.adicionar_filho(filho2)
pai.adicionar_esposa(mae)

mae.adicionar_filho(filho1)
mae.adicionar_filho(filho2)
mae.adicionar_marido(pai)
mae.adicionar_marido(amante)

filho1.adicionar_pai(pai)
filho1.adicionar_mae(mae)

filho2.adicionar_pai(pai)
filho2.adicionar_mae(mae)

# pai.resumo()
# mae.resumo()
filho1.resumo()
print()
filho2.resumo()
