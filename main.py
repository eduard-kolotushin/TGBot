import telebot
from telebot import types
from config import Config
from pyChatGPT import ChatGPT
import re

TGTOKEN = Config.TGTOKEN
GPTTOKEN = Config.GPTTOKEN

bot = telebot.TeleBot(TGTOKEN)
chat = ChatGPT(GPTTOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    # markup = types.InlineKeyboardMarkup()
    # btn = types.InlineKeyboardButton(text='This is my first own telegram bot...',
    #                                  url='')
    # markup.add(btn)
    bot.send_message(message.from_user.id, "This is my first own telegram bot...")


# @bot.message_handler(content_types=['text'])
# def reply_to_text(message):
#     txt = message.text
#     if len(re.findall(r'linux', txt, re.I)) > 0:
#         bot.send_message(message.from_user.id, "Linux related operation...")
#     else:
#         bot.send_message(message.from_user.id, "Non linux related operation...")


@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    txt = message.text
    resp = chat.send_message(txt)
    bot.send_message(message.from_user.id, resp['message'])


bot.polling(none_stop=True, interval=0)
