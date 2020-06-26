import random
import traceback
from telebot import types, TeleBot
import time
import threading
import config
import telebot
import os


bot = TeleBot('1237272474:AAFe1tAKSCPynis6P160ksddVMWFuJ3P9gA')

users = {}
finders = []

config = {
        'base_text':'Бот🧝‍♀:\n!помощь - показывает помощь\n!стоп - остановить диалог\n!новый - новый диалог\n!поиск - поиск нового диалога'
        }

def get_kb():
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton("!поиск"))
    kb.add(types.KeyboardButton("!стоп"))
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id != m.chat.id:
        return
    kb = get_kb()
    
    hello_text = "Найди себе анонимного собеседника!\nЧтобы начать поиск напиши: !поиск\nЧтобы остановить поиск напиши: !стоп\n"+\
                  "Обязательно прочитай правила использования чата: vk.cc/av2Dau"
    bot.send_message(m.chat.id, hello_text, reply_markup = kb)
    
  
def createuser(user):
    return {
        user.id:{
            'name':user.first_name,
            'id':user.id,
            'companion':None
            }
        }
  
@bot.message_handler(func = lambda m: m.text != None and m.text.lower() in ['!поиск', '!стоп'])
def command(m):
    if m.text.lower() == '!поиск':
        if m.from_user.id in users:
            bot.send_message(m.chat.id, 'Вы уже находитесь в диалоге или ищете его!')
            return
            
        users.update(createuser(m.from_user))
        user = users[m.from_user.id]
        if len(finders) > 0:
            companion = users[finders[0]]
            finders.remove(companion['id'])
            user['companion'] = companion['id']
            companion['companion'] = user['id']
            bot.send_message(user['id'], 'Бот🧝‍♀:\nСобеседник найден!')
            try:
                bot.send_message(companion['id'], 'Бот🧝‍♀:\nСобеседник найден!')
            except:
                pass
        else:
            finders.append(user['id'])
            bot.send_message(user['id'], 'Бот🧝‍♀:\nВы были помещены в очередь. Ожидайте собеседника...')
    
    elif m.text.lower() == '!стоп':
        if m.from_user.id not in users:
            bot.send_message(m.chat.id, 'Вы ещё никого не ищете! Для поиска напишите `!поиск`', parse_mode = 'markdown')
            return
            
        user = users[m.from_user.id]
        
        if user['id'] in finders:
            finders.remove(user['id'])
            bot.send_message(user['id'], 'Бот🧝‍♀:\nПоиск отменён')
            bot.send_message(user['id'], config['base_text']) 
            del users[m.from_user.id]
            return
            
        if user['companion'] != None:
            try:
                bot.send_message(user['companion'], 'Бот🧝‍♀:\nСобеседник разорвал соединение!')
                bot.send_message(user['companion'], config['base_text'])
            except:
                pass
            del users[user['companion']]
            
        bot.send_message(user['id'], 'Бот🧝‍♀:\nДиалог закончен')
        bot.send_message(user['id'], config['base_text'])    
        del users[m.from_user.id]
        
        
        
@bot.message_handler(content_types=['document'])
@bot.message_handler(content_types=['animations'])
@bot.message_handler(content_types=['text'])
@bot.message_handler(content_types=['sticker'])
@bot.message_handler(content_types=['photo'])
@bot.message_handler(content_types=['audio'])
@bot.message_handler(content_types=['voice'])
@bot.message_handler(content_types=['text'])
def texts(m):
    if m.from_user.id not in users:
        bot.send_message(m.chat.id, config['base_text'])
        return
    user = users[m.from_user.id]
    if user['companion'] == None:
        bot.send_message(m.chat.id, 'В данный момент мы ищем вам собеседника!')
        return
    else:
        dialogue(m, user['companion'])

            
def dialogue(m, companion):
    if m.text != None:
        bot.send_message(companion, m.text)
    
    elif m.photo != None:
        bot.send_photo(companion, m.photo[-1].file_id, caption = m.caption)
        
    elif m.document != None:
        bot.send_document(companion, m.document.file_id, caption = m.document.caption)
        
    elif m.animation != None:
        bot.send_document(companion, m.animation.file_id, caption = m.animation.caption)
        
    elif m.sticker != None:
        bot.send_sticker(companion, m.sticker.file_id)
        
    elif m.audio != None:
        bot.send_audio(companion, m.audio.file_id, caption = m.audio.caption)
        
    elif m.voice != None:
        bot.send_voice(companion, m.voice.file_id)
            
        
