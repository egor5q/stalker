
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

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
tokens = 'horse eats grass'
print(nltk.pos_tag(tokens.split()))
