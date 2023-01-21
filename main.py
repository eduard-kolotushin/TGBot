import telebot
from telebot import types
from config import Config
import re

TGTOKEN = Config.TGTOKEN
bot = telebot.TeleBot(TGTOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    # markup = types.InlineKeyboardMarkup()
    # btn = types.InlineKeyboardButton(text='This is my first own telegram bot...',
    #                                  url='')
    # markup.add(btn)
    bot.send_message(message.from_user.id, "This is my first own telegram bot...")


@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    txt = message.text
    if len(re.findall(r'linux', txt, re.I)) > 0:
        bot.send_message(message.from_user.id, "Linux related operation...")
    else:
        bot.send_message(message.from_user.id, "Non linux related operation...")


bot.polling(none_stop=True, interval=0)
