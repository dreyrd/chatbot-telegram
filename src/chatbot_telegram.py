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

load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER_NAME = os.getenv("USER_NAME")

TEXTO_MENU = """Olá, eu sou bot do ifsp-hto, verificador de fakes news!
    Clique em uma da ações desejadas: 
    /acao1 - Analisar link
    /acao2 - Analisar imagem
    /acao3 - Analisar mensagem"""


class TelegramBot(ChatBotBase):
    def __init__(self):
        super().__init__()
        pass


bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['number'])
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Passa seu número aí, parceiro", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Phone number', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)


@bot.message_handler(content_types=['photo'])
def photo(message):
    if message.photo is not None:
        print(message.photo)
        # verificar se tem a img no bd

        # caso n tenha, salvar no bd


@bot.message_handler(content_types=["sticker", "pinned_message", "location"])
def unhandled_message(msg):
    bot.send_message(msg.chat.id, text="Desculpa, eu não consigo responder mensagens desse tipo ainda")


@bot.message_handler(commands=["acao1"])
def acao1(msg):
    bot.send_message(msg.chat.id, "Por favor, me envia a mensagem para eu analizar")

    if msg.forward_from:
        bot.send_message(msg.chat.id, "Isso é uma mensagem encaminhada, a chance dela ser fake news é maior")
        bot.send_message(msg.chat.id, f"Mesmo assim vou verificar pra você")
        bot.send_message(msg.chat.id, "Estou analisando sua mensagem. Um momento por favor")


@bot.message_handler(commands=["acao2"])
def acao2(msg):
    md5 = hashlib.md5("Primeira mensangem".encode()).hexdigest()
    tipoMensagem = 1
    conteudo = "Primeira mensagem"
    telegramBot = TelegramBot()
    telegramBot.registrarConteudoParaAnalise(tipoMensagem, conteudo, md5)


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print('inline handler')
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.message_handler(commands=["acao3"])
def acao3(msg):
    markup = types.ForceReply(selective=False)
    message_enviada = bot.send_message(msg.chat.id, "Qual é o texto a analisar?", reply_markup=markup)
    bot.register_for_reply(message_enviada, analisar_retorno)


def analisar_retorno(x):
    texto = x.text
    telegramBot = TelegramBot()
    md5 = hashlib.md5(x.text.encode()).hexdigest()
    verificacao = telegramBot.verificarMensagem(1, texto, md5)

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
