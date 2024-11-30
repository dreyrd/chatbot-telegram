import telebot
from dotenv import load_dotenv
from telebot import types
import os
import requests
from mysql.connector import errorcode
import hashlib
from chatbot_base import ChatBotBase
import datetime
from database import Database
import requests
from bs4 import BeautifulSoup
import re
import requests
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


# Variaveis pegadas no arquivo .env, sao os dados relativos ao chatbot, caso queira alterar precisa alterar no arquivo
load_dotenv()
API_KEY = '7231801744:AAHPa6UHgZxhGsJuoBhLK5U35xszS0aY3jc'
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER_NAME = os.getenv("USER_NAME")
TEXTO_MENU = ''
ddd = None


# Informacoes sobre o banco
# verificado igual a 1 se uma pessoa ja averigou a anoticia
# fake igual a 1 se for uma noticia falsa
# justificativa e a explicacao da pessoa sobre a noticia, so e diferente de null no banco se ja foi verificado

# Esse metodo serve para saber se a mensagem se trata de um link de fato
def link_acessavel(url):
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers ,timeout=20)
        
        if response.status_code == 200:
            return True
        else:
            return False
    
    except:
        
        return False

# Verifica se o texto tem www e etc., desse modo rejeita por entender que o usuario na verdade passou um link
def eh_url(text):
    
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    
    return bool(url_pattern.match(text))

# Cria um md5 para armazenar no banco, dessa forma poupa espaco e retorna se ela ja existe no banco
def criar_md5(parametro):
    
    hash = hashlib.md5()
    hash.update(parametro.encode("utf-8"))
    return hash.hexdigest()

# Ao receber um link, o titulo que e mandado para o banco. Metodo web scrapping
def pegar_titulo(url):
    
    try:
    
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            
            titulo = soup.find('title').get_text()
            
            return titulo

    except:
        
        return 'Não foi possível acessar o link. Vamos tentar de novo?'
    
    

class TelegramBot(ChatBotBase):
    def __init__(self):
        super().__init__()
        pass

bot = telebot.TeleBot(API_KEY)
telegram_bot = TelegramBot()


# bot.message_handler (commands) se refere aos comandos do telegram, no caso abaixo /start e /help

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    cumprimento = "Olá! "
    horario = datetime.datetime.now().hour
    
    if 5 <= horario < 12:
        cumprimento += "Bom dia"
    elif 12 <= horario < 18:
        cumprimento += "Boa tarde"
    else:
        cumprimento += "Boa noite"
        
    TEXTO_MENU = f"{cumprimento}!\n\nMeu nome é <b>FakeAnalyzer</b>! 🔍\nSou um chatbot do IFSP HTO. Meu papel é <b>identificar notícias falsas</b> difundidas pelas redes sociais e pela internet, analisando e respondendo suas mensagens na forma de textos, links e imagens.\n\nDigite ou clique no comando abaixo para investigarmos:\n\n/texto\t\t- Analisar texto\t\t🔤\n\n/link\t\t- Analisar link\t\t🔗\n\n/imagem\t\t- Analisar imagem\t\t⛰"
        
    bot.send_message(msg.chat.id, TEXTO_MENU, parse_mode='HTML')
    
    if "/start" in msg.text:
        site = """
        Para mais informações sobre o projeto agente na prevenção das fakenews, confira o site:
        
        https://portalfnbook.vercel.app
        """
        
        autorizacao = "Antes de começarmos, você autoriza coletarmos seu DDD para melhorar o desempenho do bot?"
        
        bot.send_message(msg.chat.id, site)
        
        # Pergunta ao usuario se ele permite que o seu DDD seja compartilhado com o bot
         
        # Criando a estrutura de botões de "Sim" e "Não"
        markup = types.InlineKeyboardMarkup()  # Define os botões inline
        button_no = types.InlineKeyboardButton("Não", callback_data="no")    # Botão "Não"
        button_yes = types.InlineKeyboardButton("Sim", callback_data="yes")  # Botão "Sim"
        
        markup.add(button_no, button_yes)  # Adiciona os botões à estrutura
        
        # Envia a mensagem com os botões
        bot.send_message(msg.chat.id, autorizacao, reply_markup=markup)

# Função para lidar com o callback dos botões
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Mande seu contato para o bot")
    
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Entendido, não iremos utilizar seu DDD")
        

@bot.message_handler(content_types=['contact'])
def contact(msg):
    if msg.contact is not None:
        ddd = msg.contact.phone_number[2:4]
        bot.send_message(msg.message.chat.id, "DDD cadastrado com sucesso")


@bot.message_handler(content_types=["sticker", "pinned_message", "location"])
def unhandled_message(msg):
    bot.send_message(msg, "Desculpe, eu ainda não consigo responder a mensagens desse formato.")

@bot.message_handler(commands=["texto"])
def analisarTexto(msg):
    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é o texto a ser analisado?", reply_markup=markup)
    bot.register_next_step_handler(msg, analisar_retorno_texto)

@bot.message_handler(commands=["link"])
def analisarLink(msg):
    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é o link a ser analisado?", reply_markup=markup)

    if msg.forward_from:
        bot.send_message(msg.chat.id, "A mensagem, por ser encaminhada, possui chances maiores de ser falsa.")
        bot.send_message(msg.chat.id, "Só um minuto, farei uma verificação.")
        bot.send_message(msg.chat.id, "Analisando sua mensagem...")
        
    else:
        bot.register_next_step_handler(msg, analisar_retorno_link)
            

@bot.message_handler(commands=["imagem"])
def requisitarImagem(msg):
    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é a foto a ser analisado?", reply_markup=markup)

    bot.register_next_step_handler(msg, analisarImagem)


# Recebe a imagem, baixa e nomeia com a data e horario, o md5 que e inserido no banco, a imagem fica salva no disco
def analisarImagem(msg):

    if msg.photo is not None:
        if msg.content_type == 'photo':
            file_id = msg.photo[-1].file_id

            file_info = bot.get_file(file_id)

            file_path = file_info.file_path
            downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_KEY}/{file_path}").content
            
            horario = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '')

            file_name = f"{horario}.jpg"


            diretorio_salvar = "./src/images" 


            with open(f"{diretorio_salvar}/{file_name}", 'wb') as new_file:
                new_file.write(downloaded_file)
                
                md5 = criar_md5(file_name)
                
                query = f"insert into mensagem(md5, tipo, conteudo, verificado, fake, justificativa) values ('{md5}', 3, '{diretorio_salvar}/{file_name}', 0, 0, 'teste')"
                Database.executarQuery(query)
                

            bot.send_message(msg.chat.id, "Essa imagem é gerada por IA! Seus elementos foram alterados e, por isso, não deve ser confiável.")
        else:
            bot.reply_to(msg, "Conteúdo não reconhecido como imagem.")
    else:

        bot.send_message(msg.chat.id, "Não consegui compreender a mensagem enviada, envie um arquivo válido por favor.")


# Verificar se o select foi bem-sucedido
def arr_is_empty(arr):
    for element in arr:
        if element:
            return False
    return True

# Apos o usuario mandar o texto esse metodo e chamado, ele busca no banco e retorna o status do texto se ele existe

def analisar_retorno_texto(msg):
    if msg.content_type == 'text' and (not eh_url(msg.text) and not link_acessavel(msg.text)):
        texto = msg.text
        md5Atual = criar_md5(texto)
        query = f"SELECT * FROM mensagem WHERE md5 = '{md5Atual}'"
        resultado = Database.executarSelect(query)
        
        if not arr_is_empty(resultado):
            verificado = resultado[0][3]
            fake = resultado[0][4]
            justificativa = resultado[0][5]

            if(verificado):
                if(fake):
                    bot.send_message(msg.chat.id, 
                                    f"<b>O conteúdo informado é <b>FALSO!</b></b>\n\nUma análise já foi feita pelos especialistas do FakeAnalyzer e pode-se afirmar que se trata de uma informação não confiáve.\n\n<b>Justificativa:</b> {justificativa}", 
                                    parse_mode='HTML')
                else:
                    bot.send_message(msg.chat.id, 
                                    f"<b>O conteúdo informado é <b>VERDADEIRO!</b></b>\n\nUma análise já foi feita pelos especialistas do FakeAnalyzer e pode-se afirmar que se trata de uma informação confiável.\n\n<b>Justificativa:</b> {justificativa}",
                                    parse_mode='HTML')
            else:
                
                bot.send_message(msg.chat.id, "Essa mensagem já foi registrada no nosso banco, porém não foi analisada ainda")
            
        else:
            query = f"INSERT INTO mensagem(md5, tipo, conteudo) VALUES ('{md5Atual}', 1, '{msg.text}')"
            Database.executarQuery(query)
            bot.send_message(msg.chat.id, "É a primeira vez que recebemos essa mensagem. Acabamos enviá-la aos nossos especialistas, que verificarão a veracidade dessa notícia.\nPor favor, peço que verifique novamente mais tarde.")
    else:
        bot.reply_to(msg, "Conteúdo não reconhecido como texto.")

# Apos o usuario mandar o link esse metodo e chamado, ele busca no banco e retorna o status do link se ele existe

def analisar_retorno_link(msg):
    
    if link_acessavel(msg.text):
        
        texto = pegar_titulo(msg.text)
        md5Atual = criar_md5(texto)
        query = f"SELECT * FROM mensagem WHERE md5 = '{md5Atual}'"
        resultado = Database.executarSelect(query)
        
        if not arr_is_empty(resultado):
            verificado = resultado[0][3]
            fake = resultado[0][4]
            justificativa = resultado[0][5]

            if(verificado):
                if(fake):
                    bot.send_message(msg.chat.id, 
                                    f"<b>O conteúdo informado é <b>FALSO!</b></b>\n\nUma análise já foi feita pelos especialistas do FakeAnalyzer e pode-se afirmar que se trata de uma informação não confiáve.\n\n<b>Justificativa:</b> {justificativa}", 
                                    parse_mode='HTML')
                else:
                    bot.send_message(msg.chat.id, 
                                    f"<b>O conteúdo informado é <b>VERDADEIRO!</b></b>\n\nUma análise já foi feita pelos especialistas do FakeAnalyzer e pode-se afirmar que se trata de uma informação confiável.\n\n<b>Justificativa:</b> {justificativa}",
                                    parse_mode='HTML')
            else:
                
                bot.send_message(msg.chat.id, "Essa mensagem já foi registrada no nosso banco, porém não foi analisada ainda")
            
        else:
            query = f"INSERT INTO mensagem(md5, tipo, conteudo) VALUES ('{md5Atual}', 2, '{msg.text}')"
            Database.executarQuery(query)
            bot.send_message(msg.chat.id, "É a primeira vez que recebemos essa mensagem. Acabamos enviá-la aos nossos especialistas, que verificarão a veracidade dessa notícia.\nPor favor, peço que verifique novamente mais tarde.")
    
    else:
        bot.reply_to(msg, "Conteúdo não reconhecido como link.")    

bot.polling()
