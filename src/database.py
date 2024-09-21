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

DB_HOST = 'localhost'
DB_USER = 'root'
DB_NAME = 'fakeanalyzer'
DB_PASSWORD = 'Ou^4$eVpygC^t^HHwbYq'
API_KEY = '5061441215:AAE5qnFUHG6vAOjThb2wjrDAoRWPSUiGP08'
cursor = None

class DataBase:
    def __init__(self):
        self.cursor = self.db_connection.cursor(prepared=True)

    def conectar(self):
        try:
            self.db_connection = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
            database=DB_NAME)
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password is wrong")
            else:
                print('error in db')
                print('@@@@@@@@@@@@@@@@@@@')
                print(error)

    def desconectar(self):
         cursor.close()
    
    def query (self, sql, valores):
        self.conectar()
        cursor.execute(sql, valores)
        cursor.self.db_connection.commit()
        self.desconectar()

