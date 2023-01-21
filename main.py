import telebot
from telebot import types
from config import Config

TGTOKEN = Config.TGTOKEN
bot = telebot.TeleBot(TGTOKEN)


@bot.message_handlers(commands=['start'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='My VK',
                                     url='https://vk.com/eduard_kolotushin')
    markup.add(btn)
    bot.send_message(message.from_user.id, "Мой вк...", reply_markup=markup)


bot.polling(none_stop=True, interval=0)
