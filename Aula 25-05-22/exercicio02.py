class NotificaEmail():
    def __init__(self, email):
        self.email = email

    def notificar(self):
        return f"Email para {self.email}"

class NotificaWhatsapp():
    def __init__(self, numero):
        self.numero = numero

    def notificar(self):
        return f"Mensagem para {self.numero}"

class NotificaSlack():
    def __init__(self, canal):
        self.canal = canal

    def notificar(self):
        return f"Mensagem Slack: {self.canal}"

notificacoes = [
    NotificaEmail("teste@email.com"),
    NotificaWhatsapp("+5511999999999"),
    NotificaSlack("#geral")
]

for notifica in notificacoes:
    print(notifica.notificar())
