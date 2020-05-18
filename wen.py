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
db=client.wen
users=db.users
chats = db.chats

def check():
    threading.Timer(5, check).start()
    for ids in chats.find({}):
        pass
    
check()


