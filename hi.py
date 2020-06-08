from telebot import TeleBot
import config
bot = TeleBot(config.environ['hi'])


@bot.message_handler(content_types=['new_chat_members'])
def newmwm(m):
    bot.send_sticker(m.chat.id, config.hello_sticker, reply_to_message_id=m.message_id)
