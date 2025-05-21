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
        self._numero = numero
        self._saldo = saldo
    
    def sacar(self, valor: float):
        if (valor < 0):
            print("Valor negativo não é um valor valido...")
        elif (valor > self._saldo):
            print("Valor de saque invalido, maior que o da conta")
        else:
            self._saldo -= valor
            print("Valor Retirado com sucesso!")
    
    def depositar(self, valor: float):
        if (valor < 0):
            print("Valor negativo não é um valor valido")
        else:
            self._saldo += valor
            print("Valor depositado com sucesso!!!")
    
    def getNumero(self):
        return self._numero
    
    def getSaldo(self):
        return self._saldo

class ContaCorrente(ContaBancaria):
    def __init__(self, numero: int, saldo: float, agencia: int, banco: int):
        super().__init__(numero, saldo)
        self._agencia = agencia
        self._banco = banco
    
    def getAgencia(self):
        return self._agencia
    
    def getBanco(self):
        return self._banco

class ContaPoupança(ContaBancaria):
    def __init__(self, numero: int, saldo: float, taxa_juros: float):
        super().__init__(numero, saldo)
        self._taxa_juros = taxa_juros / 100
    
    def aplicarJuros(self):
        if (self._taxa_juros <= 0):
            print("Nada para fazer...")
        else:
            self._saldo *= (1 + self._taxa_juros)
    
    def getTaxaJuros(self):
        return self._taxa_juros
    
    def setTaxaJuros(self, taxa):
        if (taxa > 0):
            self._taxa_juros = taxa / 100