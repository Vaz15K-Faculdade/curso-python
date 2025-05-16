# # Exercício 3
# -------------------------------------
# https://dontpad.com/cyber130503
#
# Faça uma classe Programa com os seguinte método:
# - executar()
#
# A classe programa deve instanciar um objeto da classe Registro
# (A classe programa deve ter um atributo do tipo Registro)
# (Ao construir a classe Programa, um atributo da classe Registro deve ser criado)
#
# Através do método .executar() deverá disponibilizar um menu com as opções:
#  - adicionar ao registro, com sub-menu:
#    - pessoa
#    - professor
#    - estudante
#    - monitor
#  
#  - listar, com sub-menu:
#    - pessoa
#    - professor
#    - estudante
#    - monitor
#
# Em seguida instancie a classe e rode o método .executar()

import sys
sys.path.append('/workspaces/Aulas_Python/Aula 25-05-05')

from Exercicio01 import *
from Exercicio02 import Registro

class Programa():
    def __init__(self):
        pass

    def executar(self):
        registro = Registro()
        while True:
            print("1 - Adicionar ao Registro")
            print("2 - Listar")
            print("3 - Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.adicionar_ao_registro(registro)
            elif opcao == "2":
                self.listar(registro)
            elif opcao == "3":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def adicionar_ao_registro(self, registro):
        while True:
            print("1 - Registrar Pessoa")
            print("2 - Registrar Estudante")
            print("3 - Registrar Professor")
            print("4 - Registrar Monitor")
            print("5 - Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                registro.registrar_pessoa()
            elif opcao == "2":
                registro.registar_estudante()
            elif opcao == "3":
                registro.registar_professores()
            elif opcao == "4":
                registro.registar_monitor()
            elif opcao == "5":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def listar(self, registro):
        while True:
            print("1 - Listar Pessoas")
            print("2 - Listar Estudantes")
            print("3 - Listar Professores")
            print("4 - Listar Monitores")
            print("5 - Voltar")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                registro.listar_pessoas()
            elif opcao == "2":
                registro.listar_estudantes()
            elif opcao == "3":
                registro.listar_professores()
            elif opcao == "4":
                registro.listar_monitores()
            elif opcao == "5":
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    programa = Programa()
    programa.executar()