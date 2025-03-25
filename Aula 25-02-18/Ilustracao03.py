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

assinatura = '''
<p style="text-align: right;"><strong>Aluno da Cyber</strong></p>
<hr />
<p style="text-align: right;"><span style="color: #999999;">Aluno 10</span></p>
<p style="text-align: right;"><span style="color: #999999;">(99) 96969-6969</span></p>
'''

corpo_email += assinatura

"""-----------------------------------"""
msg = MIMEText(corpo_email, 'html')
msg['Subject'] = assunto
msg['From'] = remetente

con = SMTP_SSL(servidor, porta)
con.login(usuario, senha)
con.sendmail(remetente, dest, msg.as_string())