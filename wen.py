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
    if chats.find_one({'id':m.chat.id}) == None:
        chats.insert_one(createchat(m.chat))
    time.sleep(1)
    if m.chat.id == m.from_user.id:
        return
    memb = bot.get_chat_member(m.chat.id, m.from_user.id)
    if memb.status not in ['administrator', 'creator'] and m.from_user.id != m.chat.id:
        return
    try:
        fr = int(m.text.split(' ')[1])
    except:
        return
    if fr > 10 or fr < 0:
        bot.send_message(m.chat.id, 'Нужно число >=0 и <= 10!')
        return
    chats.update_one({'id':m.chat.id},{'$set':{'freq':fr}})
    bot.send_chat_action(m.chat.id, 'typing')
    time.sleep(3)
    bot.send_message(m.chat.id, 'Частота разговоров теперь '+str(fr)+'/10!')
 
    
@bot.message_handler(content_types=['document'], func = lambda m: m.reply_to_message != None)
@bot.message_handler(content_types=['animations'], func = lambda m: m.reply_to_message != None)
@bot.message_handler(content_types=['text'], func = lambda m: m.reply_to_message != None or (m.text != None and '@wensxur' in m.text.lower()))
@bot.message_handler(content_types=['sticker'], func = lambda m: m.reply_to_message != None)
@bot.message_handler(content_types=['photo'], func = lambda m: m.reply_to_message != None)
@bot.message_handler(content_types=['audio'], func = lambda m: m.reply_to_message != None)
@bot.message_handler(content_types=['voice'], func = lambda m: m.reply_to_message != None)
def rplyy(m):
    if chats.find_one({'id':m.chat.id}) == None:
        chats.insert_one(createchat(m.chat))
    if m.reply_to_message != None:
        if m.reply_to_message.from_user.id != 1150126466:
            return
    time.sleep(1)
    if m.reply_to_message != None:
        if m.reply_to_message.from_user.id == 1150126466:
            if '@' in m.text:
                bot.send_chat_action(m.chat.id, 'typing')
                time.sleep(3)
                bot.send_message(m.chat.id, random.choice(['Зачем ты это делаешь?']), reply_to_message_id = m.message_id)
    if random.randint(1, 100) <= 100:
        als = ['?', 'Что?', 'Почему?', 'Зачем?', 'Что такого я сделал?', 'Что случилось?', 'Что случилось']
        bot.send_chat_action(m.chat.id, 'typing')
        time.sleep(3)
        bot.send_message(m.chat.id, random.choice(als), reply_to_message_id = m.message_id)
    
@bot.message_handler(func = lambda m: True)
def chatss(m):
    if chats.find_one({'id':m.chat.id}) == None:
        chats.insert_one(createchat(m.chat))
        
    if m.text.lower()[:6] == 'привет':
        if random.randint(1, 100) <= 100:
            time.sleep(1)
            bot.send_chat_action(m.chat.id, 'typing')
            time.sleep(3)
            bot.send_message(m.chat.id, random.choice(['Расскажи, что случилось', 'Что случилось?']), reply_to_message_id = m.message_id)
            

        
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
    if random.randint(1, 100) == 10:
        act = 'teory'
    if act == 'manul':
        number = chat['manuls']
        if random.randint(1, 100) <= 30:
            number = number*random.randint(-1, 5)
            number -= random.randint(-2, 4)
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
        bot.send_chat_action(chat['id'], 'typing')
        time.sleep(3)
        bot.send_message(chat['id'], str(number)+' '+mn+'')
        chats.update_one({'id':chat['id']},{'$inc':{'manuls':random.randint(-5, 6)}})
        
    elif act == 'anzor':
        bot.send_chat_action(chat['id'], 'typing')
        time.sleep(3)                                       
        bot.send_message(chat['id'], 'Анзор')
        
    elif act == 'teory':
        txt = 'Тео́рия вероя́тностей — раздел математики, изучающий случайные события, случайные величины, их свойства и операции над ними. '+\
        'Возникновение теории вероятностей как науки относят к средним векам и первым '+\
        'попыткам математического анализа азартных игр (орлянка, кости, рулетка). Первоначально её основные понятия не '+\
        'имели строго математического вида, к ним можно было относиться как к некоторым эмпирическим фактам, как к свойствам '+\
        'реальных событий, и они формулировались в наглядных представлениях. Самые ранние работы учёных в области теории '+\
        'вероятностей относятся к XVII веку. Исследуя прогнозирование выигрыша в азартных играх, Джероламо Кардано, Блез Паскаль '+\
        'и Пьер Ферма открыли первые вероятностные закономерности, возникающие при бросании костей[1]. Под влиянием поднятых и '+\
        'рассматриваемых ими вопросов решением тех же задач занимался и Христиан Гюйгенс. При этом с перепиской Паскаля и Ферма '+\
        'он знаком не был, поэтому методику решения изобрёл самостоятельно. Его работа, в которой вводятся основные понятия теории'+\
        'вероятностей (понятие вероятности как величины шанса; математическое ожидание для дискретных случаев, в виде цены шанса), '+\
        'а также используются теоремы сложения и умножения вероятностей (не сформулированные явно), вышла в печатном виде на двадцать '+\
        'лет раньше (1657 год) издания писем Паскаля и Ферма (1679 год)[2].'
        bot.send_chat_action(chat['id'], 'typing')
        time.sleep(3)
        bot.send_message(chat['id'], txt)

def check():
    threading.Timer(10, check).start()
    for ids in chats.find({}):
        chat = ids
        if random.randint(1, 1000) <= chat['freq']*50:
            try:
                talk(chat)
            except:
                bot.send_message(441399484, traceback.format_exc())
            
    
check()


