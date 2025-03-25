from smtplib import SMTP_SSL

servidor = 'smtp.hostinger.com'
porta = 465

usuario = 'temp10@cybersocial.org.br'
senha = '@Aula321'

remetente = usuario

dest = 'wifeses804@bitflirt.com'

msg = "Teste 1"

con = SMTP_SSL(servidor, porta)
con.login(usuario, senha)
con.sendmail(remetente, dest, msg)