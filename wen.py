# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

token = os.environ['wen']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.wen
users=db.users
chats = db.chats
    
    
@bot.message_handler(commands=['set_frequency'])
def setfff(m):
    if m.chat.id == m.from_user.id:
        return
    memb = bot.get_chat_member(m.chat.id, m.from_user.id)
    if memb not in ['administrator', 'creator']:
        return
    try:
        fr = int(m.text.split(' ')[1])
    except:
        return
    if fr > 10 or fr < 0:
        bot.send_message(m.chat.id, 'Нужно число >=0 и <= 10!')
        return
    chats.update_one({'id':m.chat.id},{'$set':{'freq':fr}})
    bot.send_message(m.chat.id, 'Частота разговоров теперь '+str(fr)+'/10!')
    
@bot.message_handler(func = lambda m: m.chat.id != m.from_user.id)
def chatss(m):
    if chats.find_one({'id':m.chat.id}) == None:
        chats.insert_one(createchat(m.chat))
        

    
def createchat(chat):
    return {
        'id':chat.id,
        'title':chat.title,
        'manuls':1,
        'freq':5
    }
    
def talk(chat):
    acts = ['manul', 'anzor']
    act = random.choice(acts)
    if act == 'manul':
        number = chat['manuls']
        mn = ''
        if str(number)[-1] == '1':
            mn = 'манул'
            try:
                if str(number)[-2] == '1':
                    mn = 'манулов'
            except:
                pass
        if str(number)[-1] in ['2', '3', '4']:
            mn = 'манула'
            try:
                if str(number)[-2] == '1':
                    mn = 'манулов'
            except:
                pass
        if str(number)[-1] in ['5', '6', '7', '8', '9', '0']:
            mn = 'манулов'
        bot.send_message(chat['id'], str(number)+' '+mn+'!')
        chats.update_one({'id':chat['id']},{'$inc':{'manuls':1}})
        
    elif act == 'anzor':
                                               
        bot.send_message(chat['id'], 'Анзор'+random.choice(['.', '!', '?', '...']))

def check():
    threading.Timer(10, check).start()
    for ids in chats.find({}):
        chat = ids
        if random.randint(1, 1000) <= chat['freq']*25:
            talk(chat)
            
    
check()


