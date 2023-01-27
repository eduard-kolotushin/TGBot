import datetime
import telebot
from telebot import types
from config import Config
import openai
from utils.audio_converter import convert_audio_to_text
from utils.manager import History, Manager, Base
from utils import engine
import asyncio
import logging
from threading import Thread
import re
import os

TGTOKEN = Config.TGTOKEN
GPTTOKEN = Config.GPTTOKEN
FILEFOLDER = Config.FILEFOLDER

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


@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    txt = message.text
    # print(txt)
    logger.info(txt)
    history_txt = manager.extract_dialog(message.from_user.id)
    # print(history_txt)
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


# handler for audio from telegram
@bot.message_handler(content_types=['audio'])
def reply_to_audio(message):
    # print(message)
    file_info = bot.get_file(message.audio.file_id)
    # print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    # print(downloaded_file)
    with open(os.path.join(FILEFOLDER, "audio.ogg"), 'wb') as new_file:
        new_file.write(downloaded_file)
    # print("file saved")
    bot.send_message(message.from_user.id, "file saved")


# handler for voice from telegram
@bot.message_handler(content_types=['voice'])
def reply_to_voice(message):
    # print(message)
    file_info = bot.get_file(message.voice.file_id)
    # print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    # print(downloaded_file)
    with open(os.path.join(FILEFOLDER, "voice.ogg"), 'wb') as new_file:
        new_file.write(downloaded_file)
    text = convert_audio_to_text(FILEFOLDER, "voice.ogg")
    # print("file saved")
    resp = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=3000,
        top_p=1.0,
        frequency_penalty=0.1,
        presence_penalty=0.6
    )
    resp_str = resp["choices"][0]["text"]
    logger.info(resp_str)
    bot.send_message(message.from_user.id, resp_str)


thread = Thread(target=asyncio.run, args=(manager.run(),), daemon=True).start()
# asyncio.run_coroutine_threadsafe(manager.run())
bot.polling(none_stop=True, interval=0)
