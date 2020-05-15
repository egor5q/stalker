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
import http.cookiejar
import urllib
import urllib2
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

def polling():
    while True:
        try:
            #rq = 'https://api.telegram.org/bot'+os.environ['TELEGRAM_TOKEN']+'/getUpdates'
            req = urllib2.Request(bot+'getUpdates')
            content = OPENER.open(req).read()
            for result in json.loads(content)['result']:
                #if(result['message']['text'] == 'привет'):
                #    url = BASE_URL + 'sendMessage'
                #    req = urllib2.Request(url)
                #    req.add_header("Accept","application/json")
                #    req.add_header('User-agent',USER_AGENT)
                #    req.add_data(urllib.urlencode({'chat_id':result['message']['chat']['id'],'text':'Эй Привет чувак!'}))
                #    OPENER.open(req).read()
                print(result)
        except:
            print(traceback.format_exc())
            time.sleep(5)
        
    
    

    
              
def send_message():
    i = 'https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/sendMessage?chatid=chatid'
     
        
