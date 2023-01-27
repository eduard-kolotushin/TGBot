import datetime
import telebot
from config import Config
import openai
from utils.audio_converter import convert_audio_to_text
from utils.manager import Manager, Base
import asyncio
import logging
from threading import Thread
import os

TGTOKEN = Config.TGTOKEN
GPTTOKEN = Config.GPTTOKEN
FILEFOLDER = Config.FILEFOLDER

bot = telebot.TeleBot(TGTOKEN)
openai.api_key = GPTTOKEN
manager = Manager()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_chat_response(text):
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
    return resp_str


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.from_user.id, "This is my first own telegram bot...")


@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    txt = message.text
    logger.info(txt)
    history_txt = manager.extract_dialog(message.from_user.id)
    txt_full = txt
    if history_txt is not None:
        txt_full = "".join([history_txt, txt])
    logger.info(txt_full)
    resp_str = get_chat_response(txt_full)
    manager.add_history(chat_id=int(message.from_user.id),
                        history="\n".join([txt, resp_str]),
                        update_time=datetime.datetime.now())
    bot.send_message(message.from_user.id, resp_str)


# handler for audio from telegram
@bot.message_handler(content_types=['audio'])
def reply_to_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(os.path.join(FILEFOLDER, "audio.ogg"), 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.from_user.id, "file saved")


# handler for voice from telegram
@bot.message_handler(content_types=['voice'])
def reply_to_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(os.path.join(FILEFOLDER, "voice.ogg"), 'wb') as new_file:
        new_file.write(downloaded_file)
    history_txt = manager.extract_dialog(message.from_user.id)
    text = convert_audio_to_text(FILEFOLDER, "voice.ogg")
    txt_full = text
    if history_txt is not None:
        txt_full = "".join([history_txt, text])
    logger.info(txt_full)
    resp_str = get_chat_response(txt_full)
    bot.send_message(message.from_user.id, resp_str)


thread = Thread(target=asyncio.run, args=(manager.run(),), daemon=True).start()
bot.polling(none_stop=True, interval=0)
