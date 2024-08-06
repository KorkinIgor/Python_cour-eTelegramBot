from dotenv import load_dotenv
import telebot
import os
import webbrowser
from telebot import types

load_dotenv()

Token_name = os.getenv('TOKEN')
url_name_arbuz = os.getenv('url_arbuz')
url_name_kinopoisk = os.getenv('url_kinopoisk')
url_name_ivi = os.getenv('url_ivi')


bot = telebot.TeleBot(Token_name)


#start


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('арбуз')
    bt2 = types.KeyboardButton('кинопоиск')
    bt3 = types.KeyboardButton('иви')
    markup.row(bt1)
    markup.row(bt2, bt3)
    file = open('./photo_1.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    bot.send_message(message.chat.id, f'Игра началась {message.from_user.username}!', reply_markup=markup)
    bot.register_next_step_handler(message, reply_markup_button)


#reply_markup_button


def reply_markup_button(message):
    if message.text == 'арбуз':
        webbrowser.open(url=url_name_arbuz)
    elif message.text == 'кинопоиск':
        webbrowser.open(url=url_name_kinopoisk)
    elif message.text == 'иви':
        webbrowser.open(url=url_name_ivi)


#content_types


@bot.message_handler(content_types=['photo'])
def get_audio(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Перейти на сайт', url=url_name_arbuz)
    bt2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    bt3 = types.InlineKeyboardButton('Редоктировать', callback_data='edit')
    markup.row(bt1)
    markup.row(bt2, bt3)
    bot.reply_to(message, 'Крутое фото!', reply_markup=markup)


#callback_query_handler


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


bot.polling(non_stop=True)
