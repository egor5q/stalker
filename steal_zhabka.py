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

zhab = ['5_5']


def create_map():
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

    return locs

    
def first_turn(game):
    free_places = ['5_0', '0_5', '5_10', '10_5']
    for ids in game['players']:
        player = game['players'][ids]
        x = random.choice(free_places)
        player['pos'] = x
        game['map'][x]['players'].append(player['id'])
        free_places.remove(x)
    game['map'][zhab[0]]['objects'].append('zhabka')
    for ids in game['players']:
        player = game['players'][ids]
        kb = show_map(player, game['map'], game)
        try:
            msg = bot.send_message(player['id'], 'Тестовое отображение карты', reply_markup = kb)
            player['msg'] = msg
        except:
            bot.send_message(game['id'], 'Игрок '+player['name']+' не открыл со мной ЛС!')
            del games[game['id']]
            return
        
  
def see_pos(player, loc, code):
    pos = player['pos']
    
    x = int(pos.split('_')[0])
    y = int(pos.split('_')[1])
    i = 0
    see = False
    
    while i < 11:
        dot = str(x+i)+'_'+str(y)
        if code == dot:
            see = True
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
    
    i = 0
    while i < 11:
        dot = str(x-i)+'_'+str(y)
        if code == dot:
            see = True
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1  
        
    i = 0    
    while i < 11:
        dot = str(x)+'_'+str(y+i)
        if code == dot:
            see = True
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
        
    i = 0        
    while i < 11:
        dot = str(x)+'_'+str(y-i)
        if code == dot:
            see = True
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
        
    i = 0    
    while i < 11:
        dot = str(x+i)+'_'+str(y+i)                # вниз вправо
        if code == dot:
            see = True
            
        try:
            if 'wall' not in loc[str(x+i)+'_'+str(y+i-1)]['objects'] and 'wall' not in loc[dot]['objects']:           # проверка вверх
                if code == str(x+i+1)+'_'+str(y+i) and 'wall' not in loc[str(x+1)+'_'+str(y)]['objects']:
                    see = True
                if code == str(x+i+2)+'_'+str(y+i) and 'wall' not in loc[str(x+i+1)+'_'+str(y+i)]['objects'] and 'wall' not in loc[str(x+1)+'_'+str(y)]['objects'] and 'wall' not in loc[str(x+i+1)+'_'+str(y+i-1)]['objects']:
                    see = True
        except:
            #bot.send_message(441399484, traceback.format_exc())
            #time.sleep(0.1)
            pass
        
        try:
            if 'wall' not in loc[str(x+i-1)+'_'+str(y+i)]['objects'] and 'wall' not in loc[dot]['objects']:       # проверка влево
                if code == str(x+i)+'_'+str(y+i+1) and 'wall' not in loc[str(x)+'_'+str(y+1)]['objects']:
                    see = True
                if code == str(x+i)+'_'+str(y+i+2) and 'wall' not in loc[str(x+i)+'_'+str(y+i+1)]['objects'] and 'wall' not in loc[str(x)+'_'+str(y+1)]['objects'] and 'wall' not in loc[str(x+i-1)+'_'+str(y+i+1)]['objects']:
                    see = True
        except:
            pass
        
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
        
    i = 0    
    while i < 11:
        dot = str(x+i)+'_'+str(y-i)                # вверх вправо
        if code == dot:
            see = True
        try:
            if 'wall' not in loc[str(x+i)+'_'+str(y-i+1)]['objects'] and 'wall' not in loc[dot]['objects']:      # проверка вниз
                if code == str(x+i+1)+'_'+str(y-i) and 'wall' not in loc[str(x+1)+'_'+str(y)]['objects']:
                    see = True
                if code == str(x+i+2)+'_'+str(y-i) and 'wall' not in loc[str(x+i+1)+'_'+str(y-i)]['objects'] and 'wall' not in loc[str(x+1)+'_'+str(y)]['objects'] and 'wall' not in loc[str(x+i+1)+'_'+str(y-i+1)]['objects']:
                    see = True
        except:
            pass
        
        try:
            if 'wall' not in loc[str(x+i-1)+'_'+str(y-i)]['objects'] and 'wall' not in loc[dot]['objects']:       # проверка влево
                if code == str(x+i)+'_'+str(y-i-1) and 'wall' not in loc[str(x)+'_'+str(y-1)]['objects']:
                    see = True
                if code == str(x+i)+'_'+str(y-i-2) and 'wall' not in loc[str(x+i)+'_'+str(y-i-1)]['objects'] and 'wall' not in loc[str(x)+'_'+str(y-1)]['objects'] and 'wall' not in loc[str(x+i-1)+'_'+str(y-i-1)]['objects']:
                    see = True
        except:
            pass
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
        
    i = 0   
    while i < 11:
        dot = str(x-i)+'_'+str(y+i)                # вниз влево
        if code == dot:
            see = True
        try:
            if 'wall' not in loc[str(x-i)+'_'+str(y+i-1)]['objects'] and 'wall' not in loc[dot]['objects']:        # проверка вверх
                if code == str(x-i-1)+'_'+str(y+i) and 'wall' not in loc[str(x-1)+'_'+str(y)]['objects']:
                    see = True
                if code == str(x-i-2)+'_'+str(y+i) and 'wall' not in loc[str(x-i-1)+'_'+str(y+i)]['objects'] and 'wall' not in loc[str(x-1)+'_'+str(y)]['objects'] and 'wall' not in loc[str(x-i-1)+'_'+str(y+i-1)]['objects']:
                    see = True
        except:
            pass
        
        try:
            if 'wall' not in loc[str(x-i+1)+'_'+str(y+i)]['objects'] and 'wall' not in loc[dot]['objects']:       # проверка вправо
                if code == str(x-i)+'_'+str(y+i+1) and 'wall' not in loc[str(x)+'_'+str(y+1)]['objects']:
                    see = True
                if code == str(x-i)+'_'+str(y+i+2) and 'wall' not in loc[str(x-i)+'_'+str(y+i+1)]['objects'] and 'wall' not in loc[str(x)+'_'+str(y+1)]['objects'] and 'wall' not in loc[str(x-i+1)+'_'+str(y+i+1)]['objects']:
                    see = True
        except:
            pass
        
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1
        
    i = 0   
    while i < 11:
        dot = str(x-i)+'_'+str(y-i)                # вверх влево
        if code == dot:
            see = True
        try:
            if 'wall' not in loc[str(x-i+1)+'_'+str(y-i)]['objects'] and 'wall' not in loc[dot]['objects']:       # проверка вправо
                if code == str(x-i)+'_'+str(y-i-1) and 'wall' not in loc[str(x)+'_'+str(y-1)]['objects']:
                    see = True
                if code == str(x-i)+'_'+str(y-i-2) and 'wall' not in loc[str(x-i)+'_'+str(y-i-1)]['objects'] and 'wall' not in loc[str(x)+'_'+str(y-1)]['objects'] and 'wall' not in loc[str(x-i+1)+'_'+str(y-i-1)]['objects']:
                    see = True
        except:
            pass
        
        try:
            if 'wall' not in loc[str(x-i)+'_'+str(y-i+1)]['objects'] and 'wall' not in loc[dot]['objects']:       # проверка вниз
                if code == str(x-i-1)+'_'+str(y-i) and 'wall' not in loc[str(x-1)+'_'+str(y)]['objects']:
                    see = True
                if code == str(x-i-2)+'_'+str(y-i) and 'wall' not in loc[str(x-i-1)+'_'+str(y-i)]['objects'] and 'wall' not in loc[str(x-1)+'_'+str(y)]['objects'] and 'wall' not in loc[str(x-i-1)+'_'+str(y-i+1)]['objects']:
                    see = True
        except:
            pass
        
        if dot in loc:
            if 'wall' in loc[dot]['objects']:
                break
        i+=1 
    
    return see
        
    
        
        

        
def show_map(player, loc, game):
    radius = player['radius']
    x = int(player['pos'].split('_')[0])
    y = int(player['pos'].split('_')[1])
    start_x = x-radius
    start_y = y-radius
    end_x = x+radius
    end_y = y+radius
    
    kb = types.InlineKeyboardMarkup((radius*2)+1)
    
    while start_x <= end_x:
        start_y = y-radius
        kb_list = []
        
        while start_y <= end_y:
            code = str(start_x) + '_' + str(start_y)
            if code in loc:
                if see_pos(player, loc, code):
                    button = loctext(loc[code])
                else:
                    button = '❓'
                kb_list.append(types.InlineKeyboardButton(text = button, callback_data = 'act?'+code+'?'+str(game['id'])))
            
            else:
                kb_list.append(types.InlineKeyboardButton(text = '⬛', callback_data = 'out_map'))
            start_y+=1
          
        kb.add(*kb_list)
           
        start_x += 1
    return kb
    
def loctext(loc):
    if 'wall' in loc['objects']:
        return '⬛'
    if loc['players'] != []:
        return '🔵'
    if 'zhabka' in loc['objects']:
        return '🐸'
    
    return 'ᅠ'
    
   
@bot.message_handler(commands=['del'])
def dell(m):
    if bot.get_chat_member(m.chat.id, m.from_user.id).status in ['administrator', 'creator'] or m.from_user.id == m.chat.id:
        try:
            del games[m.chat.id]
            bot.send_message(m.chat.id, 'Игра была удалена!')
        except:
            pass
    else:
        bot.send_message(m.chat.id, 'Только администратор чата может удалить игру!')

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
        threading.Timer(0.1, first_turn, args=[game]).start()
        
     
@bot.callback_query_handler(func = lambda call: True)
def calls(call):
    try:
        if int(call.data.split('?')[2]) not in games:
            bot.answer_callback_query(call.id, 'Игры не существует!')
            return

    except:
        return
    try:
        game = games[int(call.data.split('?')[2])]
        player = game['players'][call.from_user.id]
        x = int(player['pos'].split('_')[0])
        y = int(player['pos'].split('_')[1])
        avalaible = [str(x+1)+'_'+str(y), str(x+1)+'_'+str(y+1), str(x+1)+'_'+str(y-1), str(x)+'_'+str(y+1), str(x)+'_'+str(y-1), 
                    str(x-1)+'_'+str(y), str(x-1)+'_'+str(y+1), str(x-1)+'_'+str(y-1)]
        print(player['pos'])
        for ids in avalaible:
            print(ids)
        if player['can_move']:
            if player['pos'] in avalaible:
                if 'wall' not in game['map'][call.data.split('?')[1]]['objects']:
                    game['map'][player['pos']]['players'].remove(call.from_user.id)
                    game['players'][call.from_user.id]['pos'] = call.data.split('?')[1]
                    game['map'][call.data.split('?')[1]]['players'].append(call.from_user.id)
                    for ids in game['players']:
                        try:
                            kb = show_map(game['players'][ids], game['map'], game)
                            medit('Тестовое отображение карты', game['players'][ids]['id'], game['players'][ids]['msg'].message_id, reply_markup = kb)
                        except:
                            pass
                else:
                    bot.answer_callback_query(call.id, 'Вы не можете зайти в стену!')
                    return
            else:
                bot.answer_callback_query(call.id, 'Вы не можете шагнуть так далеко!')
                return
        else:
            bot.answer_callback_query(call.id, 'Вы ещё не можете ходить!')
            return
        
    except:
        bot.answer_callback_query(call.id, 'Ошибка!')
        #bot.send_message(441399484, traceback.format_exc())

def creategame(m):
    
    return {m.chat.id:{
        'id':m.chat.id,
        'players':{},
        'turn':1,
        'text':'',
        'started':False,
        'limit':4,
        'map':create_map()
        
    }
           }
    
    
def createplayer(user):
    return {user.id:{
        'id':user.id,
        'name':user.first_name,
        'pos':None,
        'current_act':'move',
        'radius':3,
        'can_move':True,
        'msg':None
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

print('7777')
