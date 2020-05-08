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

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.lifesim
users=db.users
locs = db.locs
kvs = db.kvs

#users.update_many({},{'$set':{'power':40,
#        'maxpower':100,
#        'sleep':100,
#        'maxsleep':100}})

streets = {
    'bitard_street':{
        'name':'Битард-стрит',
        'nearlocs':['meet_street'],
        'code':'bitard_street',
        'homes':['17', '18', '30'],
        'buildings':{},
        'humans':[]
    },
    
    'new_street':{
        'name':'Новая',
        'nearlocs':['meet_street'],
        'code':'new_street',
        'homes':['101', '228'],
        'buildings':{},
        'humans':[]
    },
    
    'meet_street':{
        'name': 'Встречная',
        'nearlocs':['new_street', 'bitard_street'],
        'code':'meet_street',
        'homes':[],
        'buildings':{},
        'humans':[]
    }


}

#locs.remove({})

for ids in streets:
    street = streets[ids]
    if locs.find_one({'code':street['code']}) == None:
        locs.insert_one(street)  

letters = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 
          'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ъ', 'ы', 'э', 'ю', 'я']

emjs = ['🚶', '🚶‍♀️']

h_colors = ['brown', 'gold', 'orange', 'black']
h_lenghts = ['short', 'medium', 'long']

@bot.message_handler(commands=['clear_all'])
def clearall(m):
    if m.from_user.id == 441399484:
        users.remove({})
        bot.send_message(m.chat.id, 'Очистил юзеров.')

@bot.message_handler(commands=['navigator'])
def navv(m):
    bot.send_message(m.chat.id, '📴Проблемы с соединением, навигатор временно не работает!')
    
@bot.message_handler(commands=['help'])
def navv(m):
    bot.send_message(m.chat.id, '📴Проблемы с соединением, сайт временно не работает!')

@bot.message_handler(func = lambda message: message.text != None and message.text[0] in emjs)
def doings(m):
    if m.from_user.id != m.chat.id:
        return
    user = getuser(m.from_user)
    if m.text == '🚶Передвижение' or m.text == '🚶‍♀️Передвижение':
        avalaible_locs = []
        h = user['human']
        street = streets[h['position']['street']]
        if h['position']['flat'] == None and h['position']['building'] == None:
            for ids in street['nearlocs']:
                avalaible_locs.append('street?'+ids)
                
            for ids in street['buildings']:
                avalaible_locs.append('building?'+ids)
            
            for ids in h['keys']:
                kv = kvs.find_one({'id':int(ids.split('#')[2])})
                if kv['home'] in street['homes'] and kv['street'] == street['code']:
                        avalaible_locs.append('home?'+str(kv['id']))
                    
        else:
            avalaible_locs.append('street?'+street)
        
        if h['gender'] == 'male':
            em = '🚶'
        elif h['gender'] == 'female':
            em = '🚶‍♀️'
        kb = types.ReplyKeyboardMarkup()
            
        for ids in avalaible_locs:
            print(ids)
            kb.add(types.KeyboardButton(em+to_text(ids, 'place')))
            
        bot.send_message(m.chat.id, 'Куда хотите пойти?', reply_markup=kb)
        
    

@bot.message_handler(content_types = ['text'])
def alltxts(m):
    if m.from_user.id == m.chat.id:
        user = getuser(m.from_user)
        if user['newbie']:
            users.update_one({'id':user['id']},{'$set':{'newbie':False}})
            bot.send_message(m.chat.id, 'Здравствуй, новый житель города "Телеград". Не знаю, зачем вы сюда пожаловали, но я в чужие '+
                             'дела не лезу, как говорится. Я - Пасюк, гид в этом городе. И моя роль - заселять сюда новоприезжих, вот и всё ('+
                             'по секрету - мне за это даже не платят, хотя я стою тут 24/7 и встречаю новых людей. Делаю я это по доброте душевной '+
                             'и просто потому, что могу). '+
                             'Так что заполните анкету и сообщите мне, когда будете готовы, и я покажу вам вашу новую квартиру.')
            
            kb = getstartkb(user)
            bot.send_message(m.chat.id, 'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", '+
                                 'некоторые характеристики больше нельзя будет изменить!', reply_markup = kb)
            return
        
        if user['wait_for_stat'] != None:
            what = user['wait_for_stat']
            allow = True
            er_text = ''
            if what == 'name':
                val = m.text.title()
                for ids in m.text:
                    if ids.lower() not in letters:
                        allow = False
                        er_text = 'Имя должно содержать не более 50 символов и не может содержать ничего, кроме букв русского алфавита и пробелов!'
            elif what == 'gender':
                if m.text.lower() == 'парень':
                    val = 'male'
                if m.text.lower() == 'девушка':
                    val = 'female'
                if m.text.lower() not in ['парень', 'девушка']:
                    allow = False
                    er_text = 'Ваш пол может быть либо `парень`, либо `девушка`!'
            elif what == 'age':
                try:
                    age = int(m.text)
                    val = age
                    if age < 18 or age > 25:
                        crash += '_'
                except:
                    allow = False
                    er_text = 'Начальный возраст может быть от 18 до 25!'
            elif what == 'body.hair_color':
                if m.text.lower() == 'русый':
                    val = 'brown'
                elif m.text.lower() == 'золотой':
                    val = 'gold'
                elif m.text.lower() == 'рыжий':
                    val = 'orange'
                elif m.text.lower() == 'чёрный':
                    val = 'black'
                if m.text.lower() not in ['русый', 'золотой', 'рыжий', 'чёрный']:
                    allow = False
                    er_text = 'Цвет волос может быть `русый`, `золотой`, `рыжий` или `чёрный`!'
            elif what == 'body.hair_lenght':
                if m.text.lower() == 'короткие':
                    val = 'short'
                if m.text.lower() == 'средние':
                    val = 'medium'
                if m.text.lower() == 'длинные':
                    val = 'long'
                if m.text.lower() not in ['короткие', 'средние', 'длинные']:
                    allow = False
                    er_text = 'Длина волос может быть: `короткие`, `средние`, `длинные`!'
                    
            if allow:        
                users.update_one({'id':user['id']},{'$set':{'human.'+what:val, 'wait_for_stat':None}})    
                user = getuser(m.from_user)
            
            if allow == False:
                bot.send_message(m.chat.id, er_text, parse_mode = 'markdown')
                kb = getstartkb(user)
                bot.send_message(m.chat.id, 'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", '+
                                 'некоторые характеристики больше нельзя будет изменить!', reply_markup = kb)
            else:
                bot.send_message(m.chat.id, 'Успешно изменена выбранная характеристика на "'+str(val)+'"!')
                kb = getstartkb(user)
                bot.send_message(m.chat.id, 'Нажмите на характеристику, чтобы изменить её. Внимание! Когда вы нажмёте "✅Готово", '+
                                 'некоторые характеристики больше нельзя будет изменить!', reply_markup = kb)
                    

def getstartkb(user):
    h = user['human']
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text = 'Имя: '+str(h['name']), callback_data = 'change?name'))
    kb.add(types.InlineKeyboardButton(text = 'Пол: '+to_text(h['gender'], 'gender').lower(), callback_data = 'change?gender'))
    kb.add(types.InlineKeyboardButton(text = 'Возраст: '+str(h['age']), callback_data = 'change?age'))
    kb.add(types.InlineKeyboardButton(text = 'Наличные: '+str(h['money']), callback_data = 'change?not'))
    kb.add(types.InlineKeyboardButton(text = 'Образование: '+to_text(h['education'], 'education').lower(), callback_data = 'change?not'))
    kb.add(types.InlineKeyboardButton(text = 'Цвет волос: '+to_text(h['body']['hair_color'], 'hair_color').lower(), callback_data = 'change?body.hair_color'))
    kb.add(types.InlineKeyboardButton(text = 'Длина волос: '+to_text(h['body']['hair_lenght'], 'hair_lenght').lower(), callback_data = 'change?body.hair_lenght'))
    kb.add(types.InlineKeyboardButton(text = '✅Готово', callback_data = 'change?ready'))
    
    return kb
        
    
@bot.callback_query_handler(func = lambda call: call.data.split('?')[0] == 'change')
def changestats(call):
    user = users.find_one({'id':call.from_user.id})
    if user == None:
        return
    if user['start_stats'] == False:
        return
    what = call.data.split('?')[1]
    if what == 'not':
        bot.answer_callback_query(call.id, 'Эту характеристику изменить нельзя!', show_alert = True)
        return
    users.update_one({'id':user['id']},{'$set':{'wait_for_stat':what}})
    text = 'не определено'
    if what == 'name':
        text = 'Теперь пришлите мне ваше имя.'
    elif what == 'gender':
        text = 'Теперь пришлите мне ваш пол (может быть `парень` или `девушка`).'
    elif what == 'age':
        text = 'Теперь пришлите мне ваш возраст (от 18 до 25).'
    elif what == 'body.hair_color':
        text = 'Теперь пришлите мне цвет ваших волос (может быть: `русый`, `золотой`, `рыжий`, `чёрный`).'
    elif what == 'body.hair_lenght':
        text = 'Теперь пришлите мне длину ваших волос (могут быть: `короткие`, `средние`, `длинные`).'
        
    elif what == 'ready':
        h = user['human']
        if h['name'] == None:
            bot.answer_callback_query(call.id, 'Нельзя начать с пустым именем!', show_alert = True)
            return
        else:
            medit('Хорошо! Я вас зарегистрировал, '+h['name']+'. Ваша квартира будет находиться по адресу: улица '+
                  streets[h['street']]['name']+', дом '+h['home']+'. Надеюсь, сами доберётесь. Сейчас вы находитесь на улице Встречная! '+
                  'Чтобы найти какое-то место, вы всегда можете воспользоваться навигатором (/navigator) на своём устройстве. Успехов!', call.message.chat.id, call.message.message_id)
            
            users.update_one({'id':user['id']},{'$set':{'start_stats':False}})
                
            time.sleep(2)
            bot.send_message(call.message.chat.id, 'Чуть не забыл! По всем вопросам можете обращаться на сайт нашего города (/help). Я сам его программировал!')
            return
    medit(text, call.message.chat.id, call.message.message_id, parse_mode = 'markdown')

        
def to_text(x, param):
    ans = 'Не определено (напишите @Loshadkin)'
    if param == 'gender':
        if x == 'male':
            ans = 'Парень'
        elif x == 'female':
            ans = 'Девушка'
            
    elif param == 'education':
        if x == 'basic':
            ans = 'Общее среднее (11 классов)'
            
    elif param == 'hair_color':
        if x == 'brown':
            ans = 'Русые'
        elif x == 'gold':
            ans = 'Золотые'
        elif x == 'orange':
            ans = 'Рыжие'
        elif x == 'black':
            ans = 'Чёрные'
            
    elif param == 'hair_lenght':
        if x == 'short':
            ans = 'Короткие'
        elif x == 'medium':
            ans = 'Средние'
        elif x == 'long':
            ans = 'Длинные'
          
    elif param == 'place':
        place = x.split('?')[0]
        code = x.split('?')[1]
        if place == 'street':
            if code in ['bitard_street', 'meet_street', 'new_street']:
                ans = 'Улица '+streets[code]['name']
        if place == 'building':
            ans = 'Дом '+str(code)
        if place == 'home':
            ans = 'Квартира '+str(code)
    return ans
            
        
def human(user):
    allstrs = []
    for ids in streets:
        if len(streets[ids]['homes']) > 0:
            allstrs.append(streets[ids])
    street = random.choice(allstrs)
    home = random.choice(street['homes'])
    key = street['code']+'#'+home+'#'+str(user.id)
    return {
        'name':None,
        'gender':random.choice(['male', 'female']),
        'age':random.randint(18, 25),
        'money':random.randint(2000, 2500),
        'street':street['code'],
        'home':home,
        'keys':[key],
        'position':{
            'street':'meet_street',
            'flat':None,
            'building':None
        },
        'hunger':100,
        'maxhunger':100,
        'health':100,
        'maxhealth':100,
        'strenght':random.randint(3, 3),
        'intelligence':random.randint(3, 3),
        'power':40,
        'maxpower':100,
        'sleep':100,
        'maxsleep':100,
        'education':'basic',
        'body':{
            'hair_color':random.choice(h_colors),
            'hair_lenght':random.choice(h_lenghts),
            'height':random.randint(160, 190)
        }
        
    }    

def createuser(user):
    return {
        'id':user.id,
        'name':user.first_name,
        'username':user.username,
        'human':human(user),
        'newbie':True,
        'start_stats':True,
        'wait_for_stat':None
    }

def createkv(user, hom, street):
    return {
        'id':user.id,
        'name':user.first_name,
        'home':hom,
        'street':street
    }

def getuser(u):
    user = users.find_one({'id':u.id})
    if user == None:
        users.insert_one(createuser(u))
        user = users.find_one({'id':u.id})
        hom = user['human']['home']
        street = user['human']['street']
        kvs.insert_one(createkv(u, hom, street))
    return user

def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode=None):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)   

print('7777')
bot.polling(none_stop=True,timeout=600)

