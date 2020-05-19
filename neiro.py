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
mc = db.mc
if mc.find_one({}) == None:
    mc.insert_one({'trigger':False})
    
mc.update_one({},{'$set':{'trigger':False}})


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
            'Ю', 'Я', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '?', '«', '»', '–', '…', '—', ';']

techn = ['&', '*']

def nextsymbs():
    a = {}
    i = 10
    for ids in avalaible:
        z = ids
        if ids == '.':
            z = '^'
        if ids == '...':
            z = '#'
        cur = 1
        while cur <= i:
            try:
                a[str(cur)].update({z:0})
            except:
                a.update({str(cur):{z:0}})
            cur+=1
    for ids in techn:
        z = ids
        if ids == '.':
            z = '^'
        if ids == '...':
            z = '#'
        cur = 1
        while cur <= i:
            try:
                a[str(cur)].update({z:0})
            except:
                a.update({str(cur):{z:0}})
            cur+=1
    return a

def check():
    x = s.find_one({})
    for ids in avalaible:
        z = ids
        if ids == '.':
            z = '^'
        if ids == '...':
            z = '#'
        if z not in x:
            s.update_one({},{'$set':{z:{
                'next_symbols':nextsymbs()
            }
            }})
            
    for ids in techn:
        z = ids
        if ids == '.':
            z = '^'
        if ids == '...':
            z = '#'
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
    
    text = '&'
    lastsymbol = '&'
    ss = s.find_one({})
    i = 1
    while lastsymbol != '*' and len(text) <= 4000:
        print(lastsymbol)
        razn = 1
        ii = i
        mas = []
        itogmas = []
        s4et = 0
        while (ii - razn >= 0 and razn <= 10):
            mas.append([])
            tir = text[ii - razn]
            if tir == '.':
                tir = '^'
            for idss in ss[tir]['next_symbols'][str(razn)]:
                need = ss[tir]['next_symbols'][str(razn)][idss]
                cur = 0
                while cur < need:
                    mas[s4et].append(idss)
                    cur += 1
            s4et += 1
            razn += 1
        
        itogamount = {}
        cycle1 = 0
        for ids in mas:
            cycle2 = 0
            for idss in mas:
                cycle3 = 0
                for idsss in mas[cycle3]:
                    cycle4 = 0
                    allow = True
                    symbol = idsss
                    for idssss in mas:
                        if symbol not in mas[cycle4]:
                            allow = False
                        cycle4 += 1
                    if allow == True:
                        #if symbol not in itogmas:
                        #    itogmas.append(symbol)
                        try:
                            itogamount[symbol] += 1
                        except:
                            itogamount.update({symbol:1})
                    cycle3 += 1
                cycle2 += 1
            cycle1 += 1     
        if len(itogmas) == 0:
            try:
                bot.send_message(m.chat.id, text)
            except:
                bot.send_message(m.chat.id, 'Сообщение пустое!')
            return
        rare1 = 0
        rare2 = 0
        rare3 = 0
        word1 = None
        word2 = None
        word3 = None
        for ids in itogamount:
            if itogamount[ids] > rare1:
                rare1 = itogamount[ids]
                word1 = ids
            elif itogamount[ids] > rare2:
                rare2 = itogamount[ids]
                word2 = ids
            itogamount[ids] > rare3:
                rare3 = itogamount[ids]
                word3 = ids
        itogmas = []
        if word1 != None:
            itogmas.append(word1)
        if word2 != None:
            itogmas.append(word2)
        if word3 != None:
            itogmas.append(word3)
        cursymb = random.choice(itogmas)
        lastsymbol = cursymb
        if cursymb == '*':
            text += ''
        elif cursymb == '^':
            text += '.'
        elif cursymb == '#':
            text += '...'
        else:
            text += cursymb
        i+=1
    if len(text) > 4000:
        text = text[:4000]
    
    text = text[1:]
    try:
        bot.send_message(m.chat.id, text)
    except:
        bot.send_message(m.chat.id, 'Сообщение пустое!')
    
@bot.message_handler(content_types = ['text'])
def adds(m):
    if m.from_user.id != 441399484:
        return
    stopp = mc.find_one({})['trigger']
    while stopp == True:
        time.sleep(1)
        stopp = mc.find_one({})['trigger']
    mc.update_one({},{'$set':{'trigger':True}})
    text = '&'+m.text+'*'
    nt = m.text
    nt = nt.replace('\n', ' ').replace('"', '').replace(' ', ' ').replace('\n', ' ')
    for x in nt:
        if x not in avalaible:
            print(x)
            bot.send_message(m.chat.id, '"```'+str(x)+'```"', parse_mode = 'markdown', reply_to_message_id = m.message_id)
            mc.update_one({},{'$set':{'trigger':False}})
            return
     
    i = 0
    ss = s.find_one({})
    try:
        for x in text:
            z = x
            if x == '.':
                z = '^'
            if x == '...':
                z = '#'
            if z != '*':
                ii = i
                razn = 1
                while ii+razn < len(text) and razn <= 10:
                    nxtsmb = text[ii+razn]
                    if nxtsmb == '.':
                        nxtsmb = '^'
                    if nxtsmb == '\n':
                        nxtsmb = ' '
                    ss[z]['next_symbols'][str(razn)][nxtsmb]+=1
                    razn += 1
            i+=1
    except:
        bot.send_message(m.chat.id, traceback.format_exc(), reply_to_message_id = m.message_id)
        mc.update_one({},{'$set':{'trigger':False}})
        return
    try:
        s.remove({})
        ss.pop('_id')
        s.insert_one(ss)
        time.sleep((random.randint(1, 10)/10))
        mc.update_one({},{'$set':{'trigger':False}})
    except:
        bot.send_message(m.chat.id, traceback.format_exc(), reply_to_message_id = m.message_id)
        mc.update_one({},{'$set':{'trigger':False}})
        return
    bot.send_message(m.chat.id, 'Обработано!', reply_to_message_id = m.message_id)
        
    

            
        
  
  
