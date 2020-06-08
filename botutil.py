import time

from telebot import TeleBot


class BotUtil(TeleBot):

    def __init__(self, token, creator=None):
        super().__init__(token)
        self.bot = TeleBot(token)
        self.__group_admins = ['administrator', 'creator']
        self.__creator = creator

    def edit_message(self, message_text, chat_id, message_id, reply_markup=None, parse_mode=None):
        return self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text,
                                          reply_markup=reply_markup, parse_mode=parse_mode)

    def reply(self, chat_id, message_text, message_id, reply_markup=None, parse_mode=None):
        return self.bot.send_message(chat_id, message_text, reply_to_message_id=message_id, reply_markup=reply_markup,
                                     parse_mode=parse_mode)

    @staticmethod
    def get_link(name, user_id):
        return f'<a href="tg://user?id={user_id}">{name}</a>'

    def is_admin(self, chat, user):
        chat_member = self.bot.get_chat_member(chat, user)
        if chat_member.status in self.__group_admins:
            return True
        else:
            return False

    def report(self, text, quiet=False):
        if self.__creator:
            if not quiet:
                print(text)
            return self.bot.send_message(self.__creator, text)