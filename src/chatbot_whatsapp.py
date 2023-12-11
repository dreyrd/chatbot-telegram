from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re
import requests
import json
import mysql.connector
from mysql.connector import errorcode
import hashlib
from chatbot_base import ChatBotBase

class WhatsappBot(ChatBotBase):
    #Setamos o caminho de nossa aplicação.
    dir_path = os.getcwd()
    cssName_ContactWithNewMessage = '_3C4Vf'

    cssName_textfield = 'p3_M1' #_13NKt #_1un-p
    cssName_button = '_1Ae7k'

    cssName_messagesFromContact = 'message-in'
    cssName_forwardedMessage = 'g3ewzqzm'
    className_confirmButton = '_2Zdgs'

    cssName_ForwardedImage = 'g3ewzqzm'
    cssName_ForwardedAudio = '_2G-e-'
    cssName_ForwardedVideo = '_1C80R'

    def __init__(self):
        super().__init__()
        print("Diretorio: " + self.dir_path)
        #Setamos onde está nosso chromedriver.
        self.chrome = self.dir_path+'\\chromedriver.exe'
        #Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-data-dir="+self.dir_path+"\\profile\\wpp")
        self.options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    #def __del__(self):
        #encerra conexao com banco de dados
        #self.db_connection.close()

    def inicia(self):
         #abre conexao com banco de dados
        #Selenium irá entrar no whats e aguardar 15 segundos até o dom estiver pronto.
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        
    def verificarContatoMensagemNova(self):
        #Este pega o elemento div informando o contato que contem mensagens não lidas
        contatosComMensagem = self.driver.find_elements(By.CLASS_NAME, self.cssName_ContactWithNewMessage)
        if len(contatosComMensagem) > 0:
            self.contatoComMensagem = contatosComMensagem[0]
            return self.contatoComMensagem
        #nao ha mensagens novas
        return ''

    def localizarContato(self, nome_contato):
        print('Encontrando o contato pra clicar')
        #Selecionamos o elemento da caixa de pesquisa do whats pela classe.
        caixa_de_pesquisas = self.driver.find_elements(By.CLASS_NAME, self.cssName_textfield)
        self.caixa_de_pesquisa =  caixa_de_pesquisas[0]
        #Escreveremos o nome do contato na caixa de pesquisa e aguardaremos 2 segundos.
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        #Vamos procurar o contato/grupo que está em um span e possui o título igual que buscamos e vamos clicar.   
        contatos = self.driver.find_elements(By.XPATH, '//span[@title = "{}"]'.format(nome_contato))
        return contatos[0]

    def abreConversaContato(self, nome_contato):
        #Selecionamos o elemento da caixa de pesquisa do whats pela classe.
        caixa_de_pesquisas = self.driver.find_elements(By.CLASS_NAME, self.cssName_textfield)
        self.caixa_de_pesquisa =  caixa_de_pesquisas[0]
        #Escreveremos o nome do contato na caixa de pesquisa e aguardaremos 2 segundos.
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        #Vamos procurar o contato/grupo que está em um span e possui o título igual que buscamos e vamos clicar.   
        contatos = self.driver.find_elements(By.XPATH, '//span[@title = "{}"]'.format(nome_contato))
        self.contato[0].click()
        time.sleep(2)

    #Ao usar este método enviamos uma mensagem ao contato que está sendo visualizado
    def enviarMensagem(self, frase):
        chat_boxes = self.driver.find_elements(By.CLASS_NAME, self.cssName_textfield)
        self.caixa_de_mensagem = chat_boxes[0]
        #Escrevemos a frase na caixa de mensagem
        self.caixa_de_mensagem.send_keys(frase)
        time.sleep(1)
        #Setamos o botão de enviar e clicamos para enviar
        self.botao_enviar = self.driver.find_elements(By.CLASS_NAME, self.cssName_button)
        #comentar a linha seguinte para que nao converse com o usuario
        self.botao_enviar[0].click()
        time.sleep(1)

    def salvarArquivo(self, caminho, dados):
        with open(caminho, 'wb') as novo_arquivo:
            novo_arquivo.write(dados)
            print("Arquivo salvo em: {}".format(caminho))

    def baixarArquivoSalvar(self, url, caminho):
        resposta = requests.get(url)
        if resposta.status_code == requests.codes.OK:
            self.salvarArquivo(caminho, resposta.content)
        else:
            resposta.raise_for_status()
        return resposta

    def escuta(self):
        print('Analisando mensagens do contato')
        #Vamos obter todas as mensagens
        post = self.driver.find_elements(By.CLASS_NAME, self.cssName_messagesFromContact)
        #Mas vamos considerar apenas as 6 últimas conversas para analise
        contador = 0
        quantidadeMensagens = len(post)
        while contador < 6 and contador < quantidadeMensagens:
            print('Analisando as ultimas 6 mensagens do contato')
            ultimo = len(post) - 1 - contador
            #vamos verificar se foi uma mensagem encaminhada
            if len(post[ultimo].find_elements(By.CLASS_NAME, self.cssName_forwardedMessage)) > 0:
                print('Analisando mensagem encaminhada do contato')
                dadoVerificar = ''
                #verifica se eh texto
                if len(post[ultimo].find_elements(By.CSS_SELECTOR, 'span.selectable-text')) > 0:
                    print('Encontrei um texto a verificar')
                    tipoMensagem = 1
                    element = post[ultimo].find_element(By.CSS_SELECTOR, 'span.selectable-text')
                    texto = element.text

                    #verifica se eh um link
                    if texto[:4] == 'http':
                        #eh um link, logo o tipo muda
                        print('É um link')
                        tipoMensagem = 3

                    md5 = hashlib.md5(texto.encode()).hexdigest()
                    dadoVerificar = (tipoMensagem, texto, md5)
                #verifica se eh uma imagem
                elif len(post[ultimo].find_elements(By.CLASS_NAME, self.cssName_ForwardedImage)) > 0:
                    print('Encontrei uma imagem a verificar')
                    elemento = post[ultimo].find_element(By.TAG_NAME, 'img')
                    origem = elemento.get_attribute("src").strip()

                    print('Origem dos dados:', origem[:50])
                    
                    if origem[:4] == 'blob':
                        print("É um link de um arquivo de bytes: ", origem[5:])
                        #faz o download da imagem
                        caminhoArquivo = 'c:\\temp\\fakeanalyzer\\images\\' + origem[-36:]
                        print('Salvar o arquivo em ', caminhoArquivo)
                        dadosArquivo = self.baixarArquivoSalvar(origem[5:], caminhoArquivo)
                        #o whatsapp ja fornece o MD5
                        md5 = origem[-36:]
                    elif origem[:4] == 'data':
                        print('Sao os bytes de uma imagem')
                        tipo = origem[5:10]
                        formato = origem[11:15]
                        baseCodificacao = origem[16:22]
                        dadosArquivo = origem[24:]
                        dadosArquivo = dadosArquivo.encode('utf-8')
                        #calcula o MD5
                        md5  = hashlib.md5(dadosArquivo).hexdigest()
                        caminhoArquivo = self.dir_path + '\\images\\' + md5
                        self.salvarArquivo(caminhoArquivo, dadosArquivo)
                    else:
                        print('Nao sei o que eh...')
                        dadosArquivo = ''
                        md5 = ''
                        return (0, '3', 'Não consegui identificar a mensagem... me desculpe')
                    
                    print('Resultado do MD5: ', md5)
                    dadoVerificar = (2, '', md5)
                #verifica se eh um video
                elif len(post[ultimo].find_elements(By.CLASS_NAME, self.cssName_ForwardedVideo)) > 0:
                    print('Ainda nao aprendi a verificar vídeos... me desculpe')
                    dadoVerificar = (0, '3', 'Ainda nao aprendi a verificar videos... me desculpe')
                elif len(post[ultimo].find_elements(By.CLASS_NAME, self.cssName_ForwardedAudio)) > 0:
                    print('Ainda nao aprendi a verificar audios... me desculpe')
                    dadoVerificar = (0, '3', 'Ainda nao aprendi a verificar áudios... me desculpe')
                else:
                    dadoVerificar = (0, '1', 'Não encontrei o que analisar... Pode me encaminhar novamente a mensagem?')
                
                return dadoVerificar
            contador = contador + 1
        return  (0, '2', 'Nenhuma mensagem me foi encaminhada. Pode me encaminhar a mensagem que deseja que eu analise?')

    #Nosso método responde irá receber o parâmetro conteudo que seria o retorno do método escuta.
    def responde(self, conteudo):
        if conteudo[0] == 0:
            response = conteudo[2]
        else:
            #Setamos a reposta do bot na variável response.
            dadosVerificacao = self.verificarMensagem(conteudo[0], conteudo[1], conteudo[2])
            if dadosVerificacao[0] == False:
                #Nao ha mensagem semelhante na base de dados
                response = "Ainda não temos dados sobre essa mensagem em nossa base de dados. Mas isso não significa que seja verdade, leia atentamente e confronte com seu conhecimento, antes de encaminhar a outras pessoas."
                self.enviarMensagem(response)
                #se for uma mensagem a ser analisada, contacta o grupo 'Detetives de fake news'
                #print('Informando detetives')
                #contatoAProcessar =  self.localizarContato('Detetives de fake news')
                #contatoAProcessar.click()
                #self.enviarMensagem('Nova mensagem a verificar: ')
            else:
                print('Encontramos algo a respeito dessa mensagem em nossa base de dados')
        
                if dadosVerificacao[1] == False:
                    #mensagem ainda nao foi verificada pelos analistas
                    response = 'Esta mensagem ainda nao foi verificada por nossos analistas, logo não podemos afirmar que ela é fake ou verdadeira'
                elif dadosVerificacao[2] == True:
                    #mensagem foi verificada e eh fake
                    response = "FAKE. Esta mensagem é Fake. Para saber mais sobre, leia: " + dadosVerificacao[3]
                else: 
                    #mensagem foi verificada e nao eh fake
                    response = "A partir de nossas análises, esta mensagem não é fake news. Para saber mais sobre, leia: " + dadosVerificacao[3]
                self.enviarMensagem(response)

    def limparConversa(self, contato):
        #Right click the button to launch right click menu options
        actionChains = ActionChains(self.driver)
        actionChains.move_to_element(contato).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        time.sleep(2)
        botoes = self.driver.find_elements(By.CLASS_NAME, self.className_confirmButton)
        if len(botoes) > 0:
            print('Apagando a conversa')
            botoes[0].click()


bot = WhatsappBot()
bot.inicia()
print('inicio')
repetir = True
#Sempre será true então nunca irá para nosso script.
while repetir:
    print('analisando se há novas mensagens')
    contatoAProcessar = bot.verificarContatoMensagemNova()
    #Para testar com contatos especificos TODO comentar quando quiser analisar contatos diversos
    #contatoAProcessar =  bot.localizarContato('Meu claro')
    if contatoAProcessar != '':
        contatoAProcessar.click()
        time.sleep(2)
        #manda uma saudacao ao usuario  
        print('respondendo a uma mensagem')      
        bot.enviarMensagem('Olá! Sou o verificador de fakes! ')
        bot.enviarMensagem('Aguarde um instante que irei verificar sua mensagem')
        #Usamos o método de escuta que irá setar na variável texto.
        conteudo = bot.escuta()
        #emite uma resposta da analise do texto
        bot.responde(conteudo)
        #limpa a conversa com o contato
        #bot.limparConversa(contatoAProcessar)
    
    else:
        time.sleep(5)

del bot