import telebot
from telebot import types
from config import Config
import openai
import re

TGTOKEN = Config.TGTOKEN
GPTTOKEN = Config.GPTTOKEN

bot = telebot.TeleBot(TGTOKEN)
openai.api_key = GPTTOKEN


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
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=txt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.6
    )
    resp_str = resp["choices"][0]["text"]
    bot.send_message(message.from_user.id, resp_str)


bot.polling(none_stop=True, interval=0)
