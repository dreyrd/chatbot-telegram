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

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("")


class ChatBotBase:
    def __init__(self):
        print("caiu no ctor base")
        self.db_connection = None
        self.conectar_banco_dados()
        self.teste = "test"

    def conectar_banco_dados(self):
        print("Caiu aqui BD")
        try:
            print(DB_HOST)
            print(DB_USER)
            print(DB_NAME)
            print(DB_PASSWORD)

            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                                                         database=DB_NAME)
            print('a')

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password is wrong")
            else:
                print('error in db')
                print('@@@@@@@@@@@@@@@@@@@')
                print(error)

    def verificarMensagem(self, tipo, conteudo, md5):
        existeConteudo = False
        conteudoVerificado = False
        ehFake = False
        justificativaConteudo = ''
        cursor = self.db_connection.cursor(prepared=True)
        sql = "SELECT verificado, fake, justificativa FROM mensagem WHERE md5 = ? LIMIT 1" 
        md5value = [md5]
        cursor.execute(sql, md5value)
        for (verificado, fake, justificativa) in cursor:
            print('\n\nExiste um conteudo registrada')
            justificativaConteudo = justificativa
            existeConteudo = True
            if verificado == 1:
                conteudoVerificado = True
            if fake == 1:
                ehFake = True
        cursor.close()
        self.db_connection.commit()
        if(existeConteudo != True):
            print('Preciso aprender sobre essa nova mensagem')
            #aprende sobre a nova mensagem
            self.registrarConteudoParaAnalise(tipo, conteudo, md5)
        return (existeConteudo, conteudoVerificado, ehFake, justificativaConteudo)

    def registrarConteudoParaAnalise(self, tipo, conteudo, md5):
        cursor = self.db_connection.cursor(prepared=True)
        sql = "INSERT INTO mensagem (tipo, md5, conteudo, verificado, fake) VALUES (?, ?, ?, ?, ?)"
        values = [tipo, md5, conteudo, 0, 0]
        print('Caiu aqui no registro do bd')
        cursor.execute(sql, values)
        cursor.close()
        self.db_connection.commit()

    def registrarTeste(self):
        print('Deu certo')
        cursor = self.db_connection.cursor(prepared=True)
        sql = "INSERT INTO teste (teste) VALUES (?)"
        values = ['aaa']
        print('Caiu aqui no registro do bd')
        cursor.execute(sql, values)
        cursor.close()
        self.db_connection.commit()