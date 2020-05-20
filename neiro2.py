
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
db=client.neirotalk2
sent_types = db.senttypes
sent_to_check = db.senttocheck
words = db.words

if words.find_one({}) == None:
    words.insert_one({'words':{}})

if sent_to_check.find_one({}) == None:
    sent_to_check.insert_one({'sents':[]})
    
if sent_types.find_one({}) == None:
    sent_types.insert_one({'types':[]})
    
parts = ['существительное', 'прилагательное', 'числительное', 'глагол', 'местоимение', 'наречие', 'предикатив', 'причастие',
         'деепричастие', 'предлог', 'союз', 'частица', 'имя-название']

avalaible = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
             'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э',
            'ю', 'я',
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
             'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э',
            'Ю', 'Я', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']

znaki = [',', '.', '!', ':', '-', '?', ';']


@bot.message_handler(commands=['get_words'])
def getwords(m):
    if m.chat.id != 441399484:
        return
    x = sent_to_check.find_one({})
    for ids in x['sents']:
        added = check_predlozh(ids, True)
        if added != False and added != True:
            kb = types.InlineKeyboardMarkup()
            for ids in parts:
                kb.add(types.InlineKeyboardButton(text = ids.title(), callback_data = 'addword?'+added+'?'+ids))
            bot.send_message(m.chat.id, added, reply_markup = kb)
            
            
@bot.callback_query_handler(func = lambda call: True)
def callssss(call):
    word = call.data.split('?')[1]
    typee = call.data.split('?')[2]
    if typee != 'имя-название':
        word = word.lower()
    words.update_one({},{'$set':{'words.'+word:{'type':typee}}})
    medit('Добавлено слово "'+word+'": '+typee+'!', call.message.chat.id, call.message.message_id)
    
@bot.message_handler(commands=['new_amount'])
def newam(m):
    if m.chat.id != 441399484:
        return
    i = 0
    x = sent_to_check.find_one({})
    known = words.find_one({})
    for ids in x['sents']:
        w = ids.split()
        for idss in w:
            word = idss
            if word not in known['words']:
                i+=1
    bot.send_message(m.chat.id, 'Осталось '+str(i)+' слов!')
    
    

@bot.message_handler(content_types = ['text'])
def adds(m):
    if m.from_user.id != 441399484:
        return
    text = m.text
    for ids in text:
        if ids not in avalaible and ids not in znaki:
            bot.send_message(m.chat.id, '"'+ids+'"')
            return
    sent_to_check.update_one({},{'$push':{'sents':text}})
    bot.send_message(m.chat.id, 'Добавлено!')
    
def check_predlozh(text, newword = False):
    construct = []
    w = text.split()
    known = words.find_one({})
    for ids in w:
        word = ids
        znak = None
        if word[-1] not in avalaible:
            znak = word[-1]
            word = word[:len(word)-1]
        if word not in known['words'] and word.lower() not in known['words']:
            if newword == True:
                return word
            return False
        try:
            construct.append(known['words'][word]['type'])
        except:
            construct.append(known['words'][word.lower()]['type'])
        if znak != None:
            construct.append(znak)
      
    if construct not in sent_types.find_one({})['types']:
        sent_types.update_one({},{'$push':{'types':construct}})
    return True
        
    
def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text, reply_markup=reply_markup,
                                 parse_mode=parse_mode)
    
def check():
    threading.Timer(15, check).start()
    x = sent_to_check.find_one({})
    for ids in x['sents']:
        added = check_predlozh(ids)
        if added == True:
            sent_to_check.update_one({},{'$pull':{'sents':ids}})
            print(ids)
            
check()
    


