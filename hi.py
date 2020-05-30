import random
import traceback
from telebot import types, TeleBot
import time
import threading
import config
import telebot
import os
import config

bot = TeleBot(os.environ['hi'])


@bot.message_handler(content_types = ['sticker'])
def stikk(m):
    print(m.sticker.file_id)

@bot.message_handler(content_types = ['new_chat_member'])
def newmwm(m):
    stik = ''
    bot.send_sticker(m.chat.id, stik, reply_to_message_id = m.message_id) 

