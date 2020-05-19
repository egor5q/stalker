
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
nltk.download('averaged_perceptron_tagger')
print(nltk.pos_tag("Machine learning is great".split()))
