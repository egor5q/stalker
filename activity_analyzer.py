import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

db = MongoClient(os.environ['database']).activity_analyser
#users = db.users
chats = db.chats

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id != m.chat.id:
        countmsg(m)
        return
    text = 'Этот бот предназначен для анализа активности пользователей чатов. Он может показывать дату последнего сообщения каждого участника, считать общее число сообщений и так далее. Для начала работы добавьте меня в группу.'
    bot.send_message(m.chat.id, text, parse_mode = 'markdown')
    
    
@bot.message_handler(content_types=['document'])
@bot.message_handler(content_types=['animations'])
@bot.message_handler(content_types=['text'])
@bot.message_handler(content_types=['sticker'])
@bot.message_handler(content_types=['photo'])
@bot.message_handler(content_types=['audio'])
@bot.message_handler(content_types=['voice'])
def allmsg(m):
    if m.from_user.id == m.chat.id:
        return
    chat = createchat(m.chat)
    
    
def insertchat(chat):
    return {
        'id':chat.id,
        'name':chat.title,
        'username':chat.username,
        'users':{}
    }
    
def createchat(chat):
    chat = chats.find_one({'id':chat.id})
    if chat == None:
        chats.insert_one(insertchat(chat))
        chat = chats.find_one({'id':chat.id})
    return chat
    
    
