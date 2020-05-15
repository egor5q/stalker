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

def new_msg(result):
    if 'dice' in result['message']:
        try:
            req = urllib2.Request(bot+'sendMessage?chat_id='+str(result['message']['chat']['id'])+'&text="Брошен кубик!"')
            print(req.text)
        except:
            print(traceback.format_exc())
        
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
                new_msg(result)
        except:
            print(traceback.format_exc())
            time.sleep(5)
        
    
    

    
              
def send_message():
    i = 'https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage?chatid=chatid'
     
        
