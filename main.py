# bot_api = ""
bot_api = '' # бот для тестов
folder = 'data'
# folder = '/data'

import os
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import re
from datetime import datetime
import pytz
from flask import Flask
import sys
import threading
sys.path.append(folder)


def now_time():
    now = datetime.now()
    tz = pytz.timezone('Europe/Moscow')
    now_moscow = now.astimezone(tz)
    current_time = now_moscow.strftime("%H:%M")
    current_date = now_moscow.strftime("%m.%d.%Y")
    date = f"{current_date} {current_time}"
    return date


if not os.path.exists(f"{folder}"):
    os.makedirs(f"{folder}")
    print("Папка библиотеки создана")
# Путь к папке с базой данных
folder_path = f"{folder}"
# Название файла базы данных
db_name = "database.db"

# Проверяем существует ли файл базы данных
db_path = os.path.join(folder_path, db_name)
if os.path.exists(db_path):
    print(folder)
    print("База данных существует")
else:
    # Подключение к базе данных
    conn = sqlite3.connect(f"{folder}/database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER,
            course INTEGER,
            groupe INTEGER,
            time_registration INTEGER,
            id_message INTEGER);
        ''')
    # Закрытие соединения с базой данных
    conn.close()

bot = telebot.TeleBot(bot_api)



@bot.message_handler(commands=['start'])
def start(message):
    message_id = message.id+1
    print(message_id)
    conn = sqlite3.connect(f'{folder}/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (message.chat.id,))
    result = c.fetchone()
    if result is None:
        date_registration = now_time()
        c.execute("INSERT INTO users (user_id, course, groupe, time_registration, id_message) VALUES (?, ?, ?, ?, ?)",
                  (message.chat.id, 0, 0, date_registration, message_id))
        conn.commit()
        conn.close()
        print('Зарегистрирован новый пользователь', message.chat.id)
    else:
        c.execute(f"UPDATE users SET id_message = {(message_id)} WHERE user_id = {message.chat.id}")
        print('Пользователь' ,message.chat.id,'уже существует в базе')
        conn.commit()
        pass
    conn.close()

bot.polling()