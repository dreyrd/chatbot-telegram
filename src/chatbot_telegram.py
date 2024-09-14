import telebot
from dotenv import load_dotenv
from telebot import types
import time
import os
import re
import requests
import json
import mysql.connector
from mysql.connector import errorcode
import pyodbc
import hashlib
from chatbot_base import ChatBotBase
import time
import datetime

load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER_NAME = os.getenv("USER_NAME")





class TelegramBot(ChatBotBase):
    def __init__(self):
        print("caiu no ctor base")
        super().__init__()
        pass

bot = telebot.TeleBot(API_KEY)
telegram_bot = TelegramBot()

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    cumprimento = None
    horario = datetime.datetime.now().hour
    
    if 5 <= horario < 12:
        cumprimento = "Bom dia"
    elif 12 <= horario < 18:
        cumprimento = "Boa tarde"
    else:
        cumprimento = "Boa noite"

    TEXTO_MENU = f"""{cumprimento}! 

        Eu sou o **FakeAnalyzer** 🔍 

        Como bot do IFSP-HTO, sou um verificador de **fake news**! Meu papel é lorem ipsum dolor sit amet consectetur adiscipiscing it.

        Clique em uma da ações desejadas: 

        /texto      - Analisar texto    🔤
        /link       - Analisar link     🔗
        /imagem     - Analisar imagem   ⛰
        """
        
    bot.send_message(msg.chat.id, TEXTO_MENU)
    
    if "/start" in msg.text:
        site = """
        Nosso bot também possui um site para análise de notícias falsas e mais informações sobre o projeto
        
        link: https://sitemaneiro.com.br
        """
        
    autorizacao = "Você autorizar pegarmos seu DDD para melhorar o desempenho do bot?"
    
    bot.send_message(msg.chat.id, site)
    bot.send_message(msg.chat.id, autorizacao)
        
@bot.message_handler(commands=['start'])
def autorizar(msg):
    
    site = """
    Nosso bot também possui um site para análise de notícias falsas e mais informações sobre o projeto
    
    link: https://sitemaneiro.com.br
    """
    
    autorizacao = "Você autoriza pegarmos seu DDD para melhorar o desempenho do bot?"
    
    bot.send_message(msg.chat.id, site)
    bot.send_message(msg.chat.id, autorizacao)

@bot.message_handler(commands=['number'])
def phone(msg):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Passa seu número aí, parceiro", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(msg.chat.id, 'Phone number', reply_markup=keyboard)

# @bot.message_handler(commands=['teste'])
# def testar(msg):
#     bot.send_message(msg.chat.id, 'Anrtes')
#     telegram_bot.registrarTeste()

@bot.message_handler(content_types=['contact'])
def contact(msg):
    if msg.contact is not None:
        print(msg.contact.phone_number[:4])

@bot.message_handler(content_types=['photo'])
def photo(msg):
    if msg.photo is not None:
        print(msg.photo)
        # verificar se tem a img no bd

        # caso n tenha, salvar no bd

@bot.message_handler(content_types=["sticker", "pinned_message", "location"])
def unhandled_message(msg):
    bot.send_message(msg.chat.id, text="Desculpe, eu não consigo responder mensagens desse tipo ainda")

@bot.message_handler(commands=["texto"])
def analisarTexto(msg):
    markup = types.ForceReply(selective=False)
    message_enviada = bot.send_message(msg.chat.id, "Qual é o texto a analisar?", reply_markup=markup)
    bot.register_for_reply(message_enviada, analisar_retorno)

@bot.message_handler(commands=["link"])
def analisarLink(msg):
    bot.send_message(msg.chat.id, "Por favor, envie-me a mensagem para eu analizar")

    if msg.forward_from:
        bot.send_message(msg.chat.id, "Isso é uma mensagem encaminhada, a chance dela ser fake news é maior")
        bot.send_message(msg.chat.id, "Mesmo assim vou verificar pra você")
        bot.send_message(msg.chat.id, "Estou analisando sua mensagem. Um momento por favor")



@bot.message_handler(commands=["imagem"])
def requisitarImagem(msg):
    # md5 = hashlib.md5("Primeira mensagem".encode()).hexdigest()
    # tipoMensagem = 1
    # conteudo = "Primeira mensagem"
    # telegram_bot.registrarConteudoParaAnalise(tipoMensagem, conteudo, md5)

    markup = types.ForceReply(selective=False)
    bot.send_message(msg.chat.id, "Por favor envie a foto que será analisada", reply_markup=markup)

    bot.register_next_step_handler(msg, analisarImagem)


def analisarImagem(msg):

    if msg.photo is not None:
        # Obter o arquivo_id da imagem com a maior resolução
        file_id = msg.photo[-1].file_id

        # Obter informações do arquivo da imagem
        file_info = bot.get_file(file_id)

        # Baixar o arquivo da imagem
        file_path = file_info.file_path
        downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_KEY}/{file_path}").content

        # Definir o nome do arquivo da imagem (opcional)
        file_name = f"imagem_{msg.date.timestamp()}.jpg"

        # Diretório para salvar a imagem
        diretorio_salvar = "./src/images"  # Substitua pelo caminho correto

        # Salvar a imagem no diretório
        with open(f"{diretorio_salvar}/{file_name}", 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(msg.chat.id, "Imagem salva com sucesso!")
    else:

        bot.send_message(msg.chat.id, "Não consegui compreender a mensagem enviada, por favor envie uma foto")



@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print('inline handler')
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


def arr_is_empty(arr):
    for (element) in arr:
        if (element == True):
            return False
    return True


def analisar_retorno(x):
    texto = x.text
    md5 = hashlib.md5(x.text.encode()).hexdigest()
    verificacao = telegram_bot.verificarMensagem(1, texto, md5)

    # refazer lógica partindo do seguinte: 
    # 1 - texto está no nosso banco de dados? --> a mensagem nunca foi recebida?
    # 2 - texto foi verificado? --> fake / vdd + justificativa
    
    
    # 1 - array falso: nao achou no banco
    if (arr_is_empty(verificacao) == True):
        print('nao tem no bd')
    else:
        print('tem no bd')
        # texto foi verificado?
        # texto ja foi dito fake?
    

    if (verificacao[3] and verificacao[2]):
        bot.send_message(x.chat.id, "Essa mensagem é falsa")
        bot.send_message(x.chat.id, "Conteudo verificado")
        bot.send_message(x.chat.id, "Justificativa: " + verificacao[3])
    else:
        bot.send_message(x.chat.id, "Essa mensagem é verificada")
    pass


def verificar(msg):
    if isForwardMessage(msg):
        print(msg.forward_from.first_name)
    else:
        if isNotAPreDefinedMessage(msg):
            # print(msg)
            pass
    return True


# verica se a msg é forward ou não
def isForwardMessage(msg):
    return True if msg.forward_from else False


def isNotAPreDefinedMessage(msg):
    if (msg.text != ["acao1", "acao2", "acao3", "acao4"]):
        return True
    else:
        return False


@bot.message_handler(commands=['oi'])
def responder(msg):
    bot.reply_to(msg, TEXTO_MENU)


@bot.message_handler(commands=['exemplo'])
def enviar_msg(msg):
    bot.reply_to(msg, "Olá, tudo bem?")


bot.polling()
