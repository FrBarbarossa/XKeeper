import telebot
from telebot import types
import pprint

bot = telebot.TeleBot('token')


@bot.message_handler(commands=['start'])
def get_started(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру

    if message.text == '/start':
        bot.send_message(message.from_user.id, text='Продолжим, путник?', reply_markup=keyboard)


@bot.message_handler(content_types=['text', 'sticker'])
def get_message(message):
    print(message)
    if message.content_type == 'text':
        bot.reply_to(message, message.text)
    else:
        bot.send_message(message.from_user.id, 'Моя твоя не понимать, давай буквами')


@bot.callback_query_handler(func=lambda call: True)
def catcher(call):
    print(call.data)
    if call.data:
        print(call.message.json['reply_markup']['inline_keyboard'])


bot.infinity_polling()
