import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

db = MongoClient(os.environ['database']).activity_analyser
users = db.users

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
    chat = chats.find_one({'id':m.chat.id})
    
    
def insertuser(user):
    return {
        'id':user.id,
        'name':user.first_name
    }
    
def createuser(user):
    user = users.find_one({'id':user.id})
    if user == None:
        users.insert_one(insertuser(user))
        user = users.find_one({'id':user.id})
    return user
