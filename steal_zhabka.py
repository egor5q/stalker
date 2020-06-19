import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

db = MongoClient(os.environ['database']).ultimate_war
users = db.users

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id != m.chat.id:
        return
    user = users.find_one({'id':user.id})
    if user == None:
        text = 'Игра "укради жабку"! Ваша цель - первым утащить жабку из центра комнаты и не дать сделать это вашим оппонентам!'
        bot.send_message(m.chat.id, text, parse_mode = 'markdown')
    user = createuser(m.from_user)
    
    
def insertuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'date':time.time()
    }
    
def createuser(user):
    user = users.find_one({'id':user.id})
    if user == None:
        users.insert_one(insertuser(user))
        user = users.find_one({'id':user.id})
    return user
