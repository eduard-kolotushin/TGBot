import datetime
import telebot
from telebot import types
from config import Config
import openai
from utils.manager import History, Manager, Base
from utils import engine
import asyncio
import logging
from threading import Thread
import re

TGTOKEN = Config.TGTOKEN
GPTTOKEN = Config.GPTTOKEN

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
bot = telebot.TeleBot(TGTOKEN)
openai.api_key = GPTTOKEN
manager = Manager()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


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
    print(txt)
    logger.info(txt)
    history_txt = manager.extract_dialog(message.from_user.id)
    print(history_txt)
    txt_full = txt
    logger.info(txt_full)
    if history_txt is not None:
        txt_full = "".join([history_txt, txt])
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=txt_full,
        temperature=0.7,
        max_tokens=3000,
        top_p=1.0,
        frequency_penalty=0.3,
        presence_penalty=0.6
    )
    resp_str = resp["choices"][0]["text"]
    logger.info(resp_str)
    history = History(chat_id=int(message.from_user.id),
                      history="\n".join([txt, resp_str]),
                      update_time=datetime.datetime.now())
    manager.add_history(history)
    bot.send_message(message.from_user.id, resp_str)


thread = Thread(target=asyncio.run, args=(manager.run(),), daemon=True).start()
# asyncio.run_coroutine_threadsafe(manager.run())
bot.polling(none_stop=True, interval=0)
