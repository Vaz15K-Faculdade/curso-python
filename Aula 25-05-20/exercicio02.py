# https://dontpad.com/cyber20052
# Implemente as seguintes classes:
# 
# classe ContaBancaria com os seguintes atributos:
# - numero : int 
# - saldo : float
#
# e com os seguintes métodos:
# - sacar(valor): subtrai o valor do saldo
# - depositar(valor): incrementa o valor do saldo
#
# classe ContaCorrente que herda de ContaBancaria, com atributos:
# - agencia : código int da agência
# - banco : código int do banco
#
# classe ContaPoupanca que herda de ContaBancaria, com atributos:
# - taxa_de_juros : taxa de juros mensal (float) Ex.: 0.5 = 0,5% a.m 
# e métodos:
# - aplicar_juros(): aplica o juros sobre o saldo da conta
#
# Todos os atributos devem ser PROTEGIDOS.
# no método sacar(valor) verifique se o valor é maior que 0 e menor que o saldo da conta
# no método depositar(valor) verifique se o valor é maior que 0


class ContaBancaria():
    def __init__(self, numero: int, saldo: float):
        self.__numero = numero
        self.__saldo = saldo
    
    def sacar(self, valor: float):
        if (valor < 0):
            print("Valor negativo não é um valor valido...")
        elif (valor > self.__saldo):
            print("Valor de saque invalido, maior que o da conta")
        else:
            self.__saldo -= valor
            print("Valor Retirado com sucesso!")
    
    def depositar(self, valor: float):
        if (valor < 0):
            print("Valor negativo não é um valor valido")
        else:
            self.__saldo += valor
            print("Valor depositado com sucesso!!!")
    
    def getNumero(self):
        return self.__numero
    
    def getSaldo(self):
        return self.__saldo

class ContaCorrente(ContaBancaria):
    def __init__(self, numero: int, saldo: float, agencia: int, banco: int):
        super().__init__(numero, saldo)
        self.__agencia = agencia
        self.__banco = banco
    
    def getAgencia(self):
        return self.__agencia
    
    def getBanco(self):
        return self.__banco

class ContaPoupanca(ContaBancaria):
    def __init__(self, numero: int, saldo: float, taxa_juros: float):
        super().__init__(numero, saldo)
        self.__taxa_juros = taxa_juros / 100
    
    def aplicarJuros(self):
        if (self.__taxa_juros <= 0):
            print("Nada para fazer...")
        else:
            valor = (self.getSaldo() * (1 + self.__taxa_juros)) - self.getSaldo()
            self.depositar(valor)
    
    def getTaxaJuros(self):
        return self.__taxa_juros
    
    def setTaxaJuros(self, taxa: float):
        if (taxa > 0):
            self.__taxa_juros = taxa / 100


# Testando as classes
conta1 = ContaPoupanca(12345, 1000.0, 0.4)
conta1.aplicarJuros()

print(f"Saldo após aplicar juros: {conta1.getSaldo()}")