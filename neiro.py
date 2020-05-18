import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
    
token = os.environ['neiro']
bot = telebot.TeleBot(token)

client=MongoClient(os.environ['database'])
db=client.neirotalk
s = db.symbols

def creates():
    return {
      
    }

if s.find_one({}) == None:
    s.insert_one(creates())
    
avalaible = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
             'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э',
            'ю', 'я', ',', '.', '!', ':', ' ', '-',
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
             'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э',
            'Ю', 'Я', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

techn = ['&', '*']

def nextsymbs():
    a = {}
    for ids in avalaible:
        z = ids
        if ids == '.':
            z = '^'
        a.update({z:0})
    for ids in techn:
        z = ids
        if ids == '.':
            z = '^'
        a.update({z:0})
    return a

def check():
    x = s.find_one({})
    for ids in avalaible:
        z = ids
        if ids == '.':
            z = '^'
        if z not in x:
            s.update_one({},{'$set':{z:{
                'next_symbols':nextsymbs()
            }
            }})
            
    for ids in techn:
        z = ids
        if ids == '.':
            z = '^'
        if z not in x:
            s.update_one({},{'$set':{z:{
                'next_symbols':nextsymbs()
            }
            }})
            
check()
    
@bot.message_handler(commands=['del'])
def dellll(m):
    if m.from_user.id == 441399484:
        s.remove({})
        s.insert_one(creates())
        check()
        bot.send_message(m.chat.id, 'success')
    
@bot.message_handler(commands=['test'])
def tsttttt(m):
    if m.from_user.id != 441399484:
        return
    text = ''
    lastsymbol = '&'
    ss = s.find_one({})
    while lastsymbol != '*':
        mas = []
        for ids in ss[lastsymbol]['next_symbols']:
            z = 0
            while ss[lastsymbol]['next_symbols'][ids] > z:
                mas.append(ids)
                z += 1
        if len(mas) == 0:
            bot.send_message(m.chat.id, text)
            return
        cursymb = random.choice(mas)
        lastsymbol = cursymb
        if cursymb == '*':
            text += ''
        elif cursymb == '^':
            text += '.'
        else:
            text += cursymb
            
    bot.send_message(m.chat.id, text)
    
@bot.message_handler(content_types = ['text'])
def adds(m):
    if m.from_user.id != 441399484:
        return
    text = '&'+m.text+'*'
    for x in m.text:
        if x not in avalaible:
            bot.send_message(m.chat.id, x)
            return
     
    i = 0
    for x in text:
        z = x
        if x == '.':
            z = '^'
        if z != '*':
            nxtsmb = text[i+1]
            if nxtsmb == '.':
                nxtsmb = '^'
            s.update_one({},{'$inc':{z+'.next_symbols.'+nxtsmb:1}})
        i+=1
        
    

            
        
  
  
