class Carro():
    def __init__(self, estadoMotor, estadoMovimento):
        self.estadoMotor = estadoMotor
        self.estadoMovimento = estadoMovimento
    
    def mudarEstadoMotor(self):
        if self.estadoMotor:
            self.estadoMotor = False
        else:
            self.estadoMotor = True
    
    def mudarEstadoMovimento(self):
        if self.estadoMovimento:
            self.estadoMovimento = False
        else:
            self.estadoMovimento = True
    
    def mostrarStatus(self):
        print(f"O Motor esta {'Ligado' if self.estadoMotor else 'Desligado'}")
        print(f"O Carro esta {'Movimento' if self.estadoMovimento else 'Parado'}")

carrinho = Carro(False, False)

carrinho.mostrarStatus()
print()

carrinho.mudarEstadoMotor()
carrinho.mostrarStatus()
print()

carrinho.mudarEstadoMovimento()
carrinho.mostrarStatus()