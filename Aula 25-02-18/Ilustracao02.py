from smtplib import SMTP_SSL
from email.mime.text import MIMEText

servidor = 'smtp.hostinger.com'
porta = 465

usuario = 'temp10@cybersocial.org.br'
senha = '@Aula321'

remetente = usuario

dest = 'wifeses804@bitflirt.com'

"""-----------------------------------"""
corpo_email = 'Testando email'
assunto = 'Aula 18-02-2025'

msg = MIMEText(corpo_email, 'plain')
msg['Subject'] = assunto
msg['From'] = remetente

con = SMTP_SSL(servidor, porta)
con.login(usuario, senha)
con.sendmail(remetente, dest, msg.as_string())