import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
import json
import requests
import http.cookiejar as cookielib
import urllib
import urllib.request as urllib2
CJ = cookielib.LWPCookieJar()
from requests.exceptions import HTTPError

client=MongoClient(os.environ['database'])
db=client.dices
users=db.users

OPENER = urllib2.build_opener(urllib2.HTTPCookieProcessor(CJ))
bot = 'https://api.telegram.org/bot'+os.environ['dicebot']+'/'

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
    except HTTPError as http_err:
        print('HTTP error occurred: '+str(http_err))
    except Exception as err:
        print('Other error occurred: '+str(err))  
    else:
        print('Success!')
        
u_id = 0
ems = ['🎲', '🏀', '🎯']

def createuser(user):
    return {
        'id':user['id'],
        'name':user['first_name'],
        'results':{
            'ball':{
                'score_sum':0,
                'score_amount':0,
                '1':0,
                '2':0,
                '3':0,
                '4':0,
                '5':0
            },
            'darts':{
                'score_sum':0,
                'score_amount':0,
                '1':0,
                '2':0,
                '3':0,
                '4':0,
                '5':0,
                '6':0
            },
            'cube':{
                'score_sum':0,
                'score_amount':0,
                '1':0,
                '2':0,
                '3':0,
                '4':0,
                '5':0,
                '6':0
            }
        }
    }

if users.find_one({'id':'bot'}) == None:
    users.insert_one(createuser({'id':'bot', 'first_name': 'Dices'}))

def new_msg(result):
    user = users.find_one({'id':result['message']['from']['id']})
    if result['message']['from']['id'] == 1255836783:
        user = users.find_one({'id':'bot'})
    if user == None:
        users.insert_one(createuser(result['message']['from']))
        user = users.find_one({'id':result['message']['from']['id']})
    if 'dice' in result['message']:
        try:
            number = result['message']['dice']['value']
            em = result['message']['dice']['emoji']
            if em == '🎯':
                x = 2.5
                rs = 'darts'
                doptxt = 'дротик'
            elif em == '🎲':
                x = 3.3
                rs = 'cube'
                doptxt = 'кубик'
            elif em == '🏀':
                x = 4
                rs = 'ball'
                doptxt = 'мяч'
                
            #req = urllib2.Request(bot+'sendMessage?chat_id='+str(result['message']['chat']['id'])+'&text="Брошен кубик!"')
            time.sleep(x)
            if user['id'] != 'bot':
                req = requests.get(bot+'sendMessage?chat_id='+str(result['message']['chat']['id'])+'&text=Брошен '+doptxt+'! Результат: '+str(number)+'&reply_to_message_id='+str(result['message']['message_id']))
            users.update_one({'id':user['id']},{'$inc':{'results.'+rs+'.score_sum':number, 'results.'+rs+'.score_amount':1, str(number):number}}) 

        except:
            print(traceback.format_exc())
            
    else:
        if 'text' in result['message']:
            text = result['message']['text']
            if text.lower()[:5] == '/dice' or text.lower()[:20] == '/dice@dice_saver_bot':
                try:
                    em = text.split(' ')[1]
                except:
                    em = random.choice(ems)
                try:
                    item = text.split(' ')[1]
                    if item.lower() in ['darts', 'дартс', 'дротик']:
                        em = '🎯'
                    if item.lower() in ['bowling', 'боулинг', 'мяч', 'мячик', 'корзина']:
                        em = '🏀'
                    if item.lower() in ['cube', 'куб', 'кубик', 'кости']:
                        em = '🎲'
                except:
                    pass
                if em not in ems:
                    em = random.choice(ems)
                try:
                    req = requests.get(bot+'sendDice?chat_id='+str(result['message']['chat']['id'])+'&emoji='+em+'&reply_to_message_id='+str(result['message']['message_id']))
                    #content = OPENER.open(req).read()
                    msg = json.loads(req.text)['result']
                    print(msg)
                    new_msg(msg)
                except:
                    print(traceback.format_exc())
                    
            elif text.lower()[:9] == '/my_dices' or text.lower()[:24] == '/my_dices@dice_saver_bot':
                txt = ''
                txt += 'Статистика бросков '+user['name']+':\n\n'
                txt += '🎲:\n'
                txt += '   Количество бросков: '+str(user['results']['cube']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['cube']['score_sum']/user['results']['cube']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                    
                txt += '\n'
                txt += '🎯:\n'
                txt += '   Количество бросков: '+str(user['results']['darts']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['darts']['score_sum']/user['results']['darts']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                
                txt += '\n'
                txt += '🏀:\n'
                txt += '   Количество бросков: '+str(user['results']['ball']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['ball']['score_sum']/user['results']['ball']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                    
                req = requests.get(bot+'sendMessage?chat_id='+str(result['message']['chat']['id'])+'&text='+txt+'&reply_to_message_id='+str(result['message']['message_id']))
            
            elif text.lower()[:10] == '/bot_dices' or text.lower()[:25] == '/bot_dices@dice_saver_bot':
                user = users.find_one({'id':'bot'})
                txt = ''
                txt += 'Статистика бросков '+user['name']+':\n\n'
                txt += '🎲:\n'
                txt += '   Количество бросков: '+str(user['results']['cube']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['cube']['score_sum']/user['results']['cube']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                    
                txt += '\n'
                txt += '🎯:\n'
                txt += '   Количество бросков: '+str(user['results']['darts']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['darts']['score_sum']/user['results']['darts']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                
                txt += '\n'
                txt += '🏀:\n'
                txt += '   Количество бросков: '+str(user['results']['ball']['score_amount'])+'\n'
                try:
                    txt += '   Средний балл: '+str(round(user['results']['ball']['score_sum']/user['results']['ball']['score_amount'], 3))+'\n'
                except:
                    txt += '   Средний балл: 0\n'
                    
                req = requests.get(bot+'sendMessage?chat_id='+str(result['message']['chat']['id'])+'&text='+txt+'&reply_to_message_id='+str(result['message']['message_id']))
            

        
def polling():
    global u_id
    while True:
        try:
            #rq = 'https://api.telegram.org/bot'+os.environ['TELEGRAM_TOKEN']+'/getUpdates'
            req = urllib2.Request(bot+'getUpdates?offset='+str(u_id))
            content = OPENER.open(req).read()
            for result in json.loads(content)['result']:
                u_id = result['update_id']+1
                #if(result['message']['text'] == 'привет'):
                #    url = BASE_URL + 'sendMessage'
                #    req = urllib2.Request(url)
                #    req.add_header("Accept","application/json")
                #    req.add_header('User-agent',USER_AGENT)
                #    req.add_data(urllib.urlencode({'chat_id':result['message']['chat']['id'],'text':'Эй Привет чувак!'}))
                #    OPENER.open(req).read()
                print(result)
                threading.Thread(target = new_msg, args = [result]).start()
        except:
            print(traceback.format_exc())
            time.sleep(5)
        
    
    

    
              
def send_message():
    i = 'https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage?chatid=chatid'
     
        
