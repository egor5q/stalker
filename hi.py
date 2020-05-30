import random
import traceback
from telebot import types, TeleBot
import time
import threading
import telebot
import os

bot = TeleBot(os.environ['hi'])


@bot.message_handler(content_types = ['sticker'])
def stikk(m):
    print(m.sticker.file_id)

@bot.message_handler(content_types = ['new_chat_member'])
def newmwm(m):
    stik = 'CAACAgIAAxkBAAMCXtJFY5hU1RjGiF-2TfdqH_qB1QcAAh8AA51v8gKBOa_rqLp0lRkE'
    bot.send_sticker(m.chat.id, stik, reply_to_message_id = m.message_id) 

