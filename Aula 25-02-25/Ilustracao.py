import youtube_dl
import telebot

bot = telebot.TeleBot("7777510686:AAFiJO6ElZZQx9WSPLXryiwmn2gaeeLDdPc")
# bot = telebot.TeleBot(os.getenv('TOKEN_BOT_TELEGRAM'))

@bot.message_handler(commands=['start'])#, 'help'])
def mensagem_inicial(message):
    nome = bot.get_my_name()
    nome_usuario = message.from_user.first_name
    
    bot.send_message(message.chat.id, f"Ola {nome_usuario}! Eu sou o bot {nome},erei responsavel")


def processar_escolha(message):
    escolha = message.text.strip()
    
    if escolha == '1':
        bot.send_message(message.chat.id, 'Você escolheu baixar uma música.')
        bot.send_message(message.chat.id, 'Por favor, envie o link do YouTube da música:')
        bot.register_next_step_handler(message, baixar_musica)
    
    elif escolha == '2':
        bot.send_message(message.chat.id, 'Você escolheu baixar um vídeo.')
        bot.send_message(message.chat.id, 'Por favor, envie o link do YouTube do vídeo:')
        bot.register_next_step_handler(message, baixar_video)
    
    else:
        bot.send_message(message.chat.id, 'Opção inválida. Por favor, escolha 1 para música ou 2 para vídeo.')
        bot.send_message(message.chat.id, '1 - Música\n2 - Vídeo')
        bot.register_next_step_handler(message, processar_escolha)

def baixar_video(message):
    link = message.text.strip()
    bot.send_message(message.chat.id, f'Iniciando download da Video')

    # Opções para baixar vídeo
    opcoes = {
        'format': 'best[height<=720]',  # Limitando qualidade para evitar arquivos muito grandes
        'outtmpl': 'video_%(title)s.%(ext)s',
        'noplaylist': True,
    }
    
    with youtube_dl.YoutubeDL(opcoes) as ytdl:
        info = ytdl.extract_info(link, download=True)
        titulo = info.get('title', 'musica')
        nome_arquivo = f"video_{titulo}.{info.get('ext', 'mp4')}"
        
    # Enviando o arquivo para o usuário
    with open(nome_arquivo, 'rb') as video:
        bot.send_video(message.chat.id, video, caption=f"Video: {titulo}")


def baixar_musica(message):
    link = message.text.strip()
    bot.send_message(message.chat.id, f'Iniciando download da Música')

    opcoes = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'musica_%(title)s.%(ext)s',
            'noplaylist': True,
        }

    with youtube_dl.YoutubeDL(opcoes) as ytdl:
        info = ytdl.extract_info(link, download=True)
        titulo = info.get('title', 'musica')
        nome_arquivo = f"musica_{titulo}.mp3"
        
    # Enviando o arquivo para o usuário
    with open(nome_arquivo, 'rb') as audio:
        bot.send_audio(message.chat.id, audio, caption=f"Música: {titulo}")


@bot.message_handler(commands=['baixar'])
def baixar(message):
    bot.send_message(message.chat.id, 'O que você quer baixar?')
    bot.send_message(message.chat.id, '1 - Música\n2 - Vídeo')
    bot.register_next_step_handler(message, processar_escolha)


@bot.message_handler(commands=['sair'])
def sair(message):
    bot.reply_to(message, 'OK, :(')

# roda o TeleBot
bot.infinity_polling()
