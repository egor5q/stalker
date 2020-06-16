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
        text = 'Война... Что может быть хуже? Верно - бесконечная война... Сюда попадают души тех, кого не приняли ни в рай, ни даже в ад. '+\
        'Именно здесь им суждено провести *ВЕЧНОСТЬ.* Убей, или будь убит! Но они даже не могут умереть. После смерти они вновь появляются в этом месте. '+\
        'Эдакая тюрьма для тех, кто не угодил высшим силам. И вы будете исполнять роль одной из таких душ. Не знаю, как, но Пасюк договорился '+\
        'с нашим начальством по этому поводу... Но я теперь обязан выдать вам тело. Что бы с ним не случилось, после перерождения оно примет прежнюю '+\
        'форму. Пользуйтесь... Ах да, я не представился. Да и не должен был. Всего хорошего!'
        bot.send_message(m.chat.id, text, parse_mode = 'markdown')
    user = createuser(m.from_user)
    
    
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
