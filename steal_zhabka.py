import os
import telebot
import time
import random
import threading
from telebot import types
from pymongo import MongoClient
import traceback

db = MongoClient(os.environ['database']).steal_zhabka
users = db.users
bot = telebot.TeleBot(os.environ['zhabka'])

games = {}

def createpos(objs = []):

    return {
        'players':[],
        'objects':objs
    }

walls = ['0_3', '0_7', '1_1', '1_3', '1_7', '1_9', '2_1', '2_5', '2_9', '3_0', '3_1', '3_3', 
        '3_5', '3_7', '3_9', '3_10', '5_2', '5_3', '5_7', '5_8', '7_0', '7_1', '7_3', '7_5', '7_7',
        '7_9', '7_10', '8_1', '8_5', '8_9', '9_1', '9_3', '9_7', '9_9', '10_3', '10_7']

locs = {}

x = 0
while x < 11:
    y = 0
    while y < 11:
        obj = []
        if str(x)+'_'+str(y) in walls:
            obj = ['wall']
        locs.update({str(x)+'_'+str(y):createpos(obj)})
        
        y+=1
    x+=1

    
def first_turn(game):
    free_places = ['5_0', '0_5', '5_10', '10_5']
    for ids in game['players']:
        player = game['players'][ids]
        x = random.choice(free_places)
        player['pos'] = x
        free_places.remove(x)
    for ids in game['players']:
        player = game['players'][ids]
        kb = show_map(player, game['map'])
        try:
            bot.send_message(player['id'], 'Тестовое отображение карты', reply_markup = kb)
        except:
            bot.send_message(game['id'], 'Игрок '+player['name']+' не открыл со мной ЛС!')
        
        
def show_map(player, loc):
    radius = player['radius']
    x = int(player['pos'].split('_')[0])
    y = int(player['pos'].split('_')[1])
    start_x = x-radius
    start_y = y-radius
    end_x = x+radius
    end_y = y+radius
    
    amount = radius*2
    code = str(start_x) + '_' + str(start_y)
    if code not in loc:
        amount -= 1
        
    code = str(start_x+1) + '_' + str(start_y)
    if code not in loc:
        amount -= 1
        
    code = str(start_x+2) + '_' + str(start_y)
    if code not in loc:
        amount -= 1

    kb = types.InlineKeyboardMarkup(amount)
    
    while start_x <= end_x:
        while start_y <= end_y:
            code = str(start_x) + '_' + str(start_y)
            if code in loc:
                kb.add(types.InlineKeyboardButton(text = loctext(loc[code]), callback_data = 'act?'+code))
    return kb
    
def loctext(loc):
    if 'wall' in loc['objects']:
        return '⬛'
    if loc['players'] != []:
        return '🔵'
    if 'zhabka' in loc['objects']:
        return '🐸'
    
    return 'ᅠ'
    
    
@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id != m.chat.id:
        return
    text = 'Игра "укради жабку"! Ваша цель - первым утащить жабку из центра комнаты и не дать сделать это вашим оппонентам!'
    bot.send_message(m.chat.id, text, parse_mode = 'markdown')
    user = createuser(m.from_user)
    
    
@bot.message_handler(commands=['join'])
def join(m):
    if m.chat.id not in games:
        bot.send_message(m.chat.id, 'Игра ещё не была создана!')
        return
    game = games[m.chat.id]
    if game['started'] == True:
        bot.send_message(m.chat.id, 'Игра уже в процессе!')
        return
    if m.from_user.id in game['players']:
        bot.send_message(m.chat.id, 'Вы уже в игре!')
        return
    if len(game['players']) >= game['limit']:
        bot.send_message(m.chat.id, 'Лимит партии - 4 игрока!')
        return
    game['players'].update(createplayer(m.from_user))
    bot.send_message(m.chat.id, m.from_user.first_name+' присоединился к игре!') 
    
@bot.message_handler(commands=['prepare_zhabka'])
def startgame(m):
    user = users.find_one({'id':m.from_user.id})
    if user == None:
        user = users.insert_one(createuser(m.from_user))
        user = users.find_one({'id':m.from_user.id})
    if m.chat.id not in games:
        game = creategame(m)
        x = m.text.split(' ')

        games.update(game)
        game = games[m.chat.id]
        bot.send_message(m.chat.id, 'Подготовка к игре запущена! Кто желает попытаться сп*здить жабку - жмём /join!')
    else:
        bot.send_message(m.chat.id, 'В этом чате уже есть игра!')
        return
    
    
@bot.message_handler(commands=['go_zhabka'])
def go(m):
    if m.chat.id not in games:
        bot.send_message(m.chat.id, 'Игра ещё не была создана!')
        return
    game = games[m.chat.id]
    if game['started'] == False:
        game['started'] = True

        bot.send_message(m.chat.id, 'Игра начинается!')
        threading.Timer(2, first_turn, args=[game]).start()
        
     
def creategame(m):
    return {m.chat.id:{
        'id':m.chat.id,
        'players':{},
        'turn':1,
        'text':'',
        'started':False,
        'limit':4,
        'map':locs.copy()
        
    }
           }
    
    
def createplayer(user):
    return {user.id:{
        'id':user.id,
        'name':user.first_name,
        'pos':None,
        'current_act':'move',
        'radius':3
    }
           }
    
    
def medit(message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                    reply_markup=reply_markup,
                                    parse_mode=parse_mode)
    
    
def insertuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'date':time.time()
    }
    
def createuser(user1):
    user = users.find_one({'id':user1.id})
    if user == None:
        users.insert_one(insertuser(user1))
        user = users.find_one({'id':user1.id})
    return user
