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


load_dotenv()

API_KEY = '7231801744:AAHPa6UHgZxhGsJuoBhLK5U35xszS0aY3jc'
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER_NAME = os.getenv("USER_NAME")
TEXTO_MENU = ''

def criar_md5(parametro):
    
    hash = hashlib.md5()
    hash.update(parametro.encode("utf-8"))
    return hash.hexdigest()

def pegar_titulo(url):
    
    try:
    
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            
            titulo = soup.find('h1').get_text()
            
            return titulo

    except:
        
        return 'Não foi possível acessar o link. Vamos tentar de novo?'
    
    

class TelegramBot(ChatBotBase):
    def __init__(self):
        super().__init__()
        pass

bot = telebot.TeleBot(API_KEY)
telegram_bot = TelegramBot()

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
        
    TEXTO_MENU = f"{cumprimento}!\n\nMeu nome é <b>FakeAnalyzer</b>! 🔍\n\Sou um chatbot do IFSP HTO. Meu papel é <b>identificar notícias falsas</b> difundidas pelas redes sociais e pela internet, analisando e respondendo suas mensagens na forma de textos, links e imagens.\n\nDigite ou clique no comando abaixo para investigarmos:\n\n/texto\t\t- Analisar texto\t\t🔤\n\n/link\t\t- Analisar link\t\t🔗\n\n/imagem\t\t- Analisar imagem\t\t⛰"
        
    bot.send_message(msg.chat.id, TEXTO_MENU, parse_mode='HTML')
    
    if "/start" in msg.text:
        site = """
        Para mais informações sobre o projeto agente na prevenção das fakenews, confira o site:
        
        https://sitemaneiro.com.br
        """
        
        autorizacao = "Antes de começarmos, você autoriza coletarmos seu DDD para melhorar o desempenho do bot?"
        
        bot.send_message(msg.chat.id, site)
        bot.send_message(msg.chat.id, autorizacao)
        
@bot.message_handler(commands=['start'])
def autorizar(msg):
    
    site = """
    Para mais informações sobre o projeto agente na prevenção das fakenews, confira o site:
        
    https://sitemaneiro.com.br
    """
    
    autorizacao = "Antes de começarmos, você autoriza coletarmos seu DDD para melhorar o desempenho do bot?"
    
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

#   //*[@id="post-1739851"]/h1

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
    bot.send_message(msg, "Desculpe, eu ainda não consigo responder a mensagens desse formato.")

@bot.message_handler(commands=["texto"])
def analisarTexto(msg):
    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é o texto a ser analisado?", reply_markup=markup)
    bot.register_next_step_handler(msg, analisar_retorno)

@bot.message_handler(commands=["link"])
def analisarLink(msg):
    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é o link a ser analisado?", reply_markup=markup)

    if msg.forward_from:
        bot.send_message(msg.chat.id, "A mensagem, por ser encaminhada, possui chances maiores de ser falsa.")
        bot.send_message(msg.chat.id, "Só um minuto, farei uma verificação.")
        bot.send_message(msg.chat.id, "Analisando sua mensagem...")
        
    else:
        bot.register_next_step_handler(msg, analisar_link)
        

def analisar_link(msg):
    
    titulo = pegar_titulo(msg.text)
    
    bot.send_message(msg.chat.id, titulo)





@bot.message_handler(commands=["imagem"])
def requisitarImagem(msg):
    # md5 = hashlib.md5("Primeira mensagem".encode()).hexdigest()
    # tipoMensagem = 1
    # conteudo = "Primeira mensagem"
    # telegram_bot.registrarConteudoParaAnalise(tipoMensagem, conteudo, md5)

    markup = types.ForceReply(selective=False)
    bot.reply_to(msg, "Qual é a foto a ser analisado?", reply_markup=markup)

    bot.register_next_step_handler(msg, analisarImagem)


def analisarImagem(msg):

    if msg.photo is not None:
        
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

        bot.send_message(msg.chat.id, "Não consegui compreender a mensagem enviada, envie um arquivo válido por favor.")



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
    for element in arr:
        if element:
            return False
    return True


def analisar_retorno(msg):
    texto = msg.text
    md5Atual = criar_md5(texto)
    query = f"SELECT * FROM mensagem WHERE md5 = '{md5Atual}'"
    resultado = Database.executarSelect(query)
    
    if not arr_is_empty(resultado):
        md5 = resultado[0][0]
        tipo = resultado[0][1]
        conteudo = resultado[0][2]
        verificado = resultado[0][3]
        fake = resultado[0][4]
        justificativa = resultado[0][5]
    else:
        query = f"INSERT INTO mensagem(md5, tipo, conteudo) VALUES ('{md5Atual}', 1, '{msg.text}')"
        Database.executarQuery(query)
    
    

    #verificacao = telegram_bot.verificarMensagem(1, texto, md5)
    # refazer lógica partindo do seguinte: 
    # 1 - texto está no nosso banco de dados? --> a mensagem nunca foi recebida?
    # 2 - texto foi verificado? --> fake / vdd + justificativa
    
    
    # 1 - array falso: nao achou no banco
    #if (arr_is_empty(verificacao) == True):
    #    print('nao tem no bd')
    #else:
    #    print('tem no bd')
        # texto foi verificado?
        # texto ja foi dito fake?
    

    #if (verificacao[3] and verificacao[2]):
    #    bot.send_message(x.chat.id, "Essa mensagem é falsa")
    #    bot.send_message(x.chat.id, "Conteudo verificado")
    #    bot.send_message(x.chat.id, "Justificativa: " + verificacao[3])
    #else:
    #    bot.send_message(x.chat.id, "Essa mensagem é verificada")
    #pass














# def verificar(msg):
#     if isForwardMessage(msg):
#         print(msg.forward_from.first_name)
#     else:
#         if isNotAPreDefinedMessage(msg):
#             # print(msg)
#             pass
#     return True


# verica se a msg é forward ou não
# def isForwardMessage(msg):
#     return True if msg.forward_from else False


# def isNotAPreDefinedMessage(msg):
#     if (msg.text != ["acao1", "acao2", "acao3", "acao4"]):
#         return True
#     else:
#         return False


bot.polling()
