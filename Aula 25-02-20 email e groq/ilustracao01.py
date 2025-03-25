from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from os.path import basename
import json

with open("config.json", "r") as arq:
    config = json.load(arq)

servidor = config["servidor"]
porta = config["porta"]
usuario = config["usuario"]
senha = config["senha"]

remetente = usuario
destinatario = "goldwileen@edny.net"
assunto = "Nao leia..."
corpo_email = """
"""

arquivos_anexo = "ex1.py"

msg = MIMEMultipart()
msg["From"] = remetente
msg["Subject"] = assunto

msg.attach(MIMEText(corpo_email))

with open(arquivos_anexo, "rb") as arq:
    part = MIMEApplication(
        arq.read(),
        Name = basename(arquivos_anexo)
    )

part["Content-Disposition"] = 'attachment; filename="%s"' % basename(arquivos_anexo)
msg.attach(part)

con = SMTP_SSL(servidor, porta)
con.login(usuario, senha)

# Modificar a linha de envio para usar o destinatário
con.sendmail(remetente, destinatario, msg.as_string())