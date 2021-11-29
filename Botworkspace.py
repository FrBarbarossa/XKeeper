import telebot
from telebot import types
import Dataworkspace as dw
import pprint

logged = []

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start', 'help', 'new'])
def get_started(message):
    if message.text == '/start':
        # print(message.from_user.id, dw.check_auth(int(message.from_user.id)))
        if not dw.check_auth(int(message.from_user.id)):
            keyboard = types.InlineKeyboardMarkup()
            key_register = types.InlineKeyboardButton(text='Регистрация', callback_data='/register')
            key_login = types.InlineKeyboardButton(text='У меня уже есть аккаунт', callback_data='/login')
            keyboard.add(key_login, key_register)
            bot.send_message(message.from_user.id,
                             text="Добро пожаловать в XKeeper! Наш бот поможет Вам не забывать о гарантийных талонах и не копить ненужную бумагу.",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, 'Вы уже авторизованы в системе')

    if message.text.startswith('/new') and not dw.check_auth(int(message.from_user.id)):
        temp_data = message.text.split()
        if len(temp_data) == 3:
            name, psw = temp_data[-2], temp_data[-1]
            if dw.insert_user(name, psw):
                logged.append(message.from_user.id)
                dw.auth(message.from_user.id, name)
                bot.send_message(message.from_user.id,
                                 text='Регистрация прошла успешно!\nВ целях безопасности советуем удалить Ваше сообщение, где Вы указали логин и пароль. Обязательно запомните эти данные для входа в аккаунт!')
            else:
                bot.send_message(message.from_user.id, 'Пользователь с таким именем уже существует, попробуйте снова')
        else:
            bot.send_message(message.from_user.id,
                             'Введите команду с корректными данными в формате: /new LOGIN PASSWORD')


@bot.message_handler(content_types=['text', ])
def get_message(message):
    print(message)
    if message.content_type == 'text':
        pass
    else:
        bot.send_message(message.from_user.id, 'Моя твоя не понимать, давай буквами')


@bot.callback_query_handler(func=lambda call: True)
def catcher(call):
    if call.data:
        if call.data == '/register':
            bot.send_message(call.from_user.id, text='Создайте Вашего пользователя с помощью /new LOGIN PASSWORD')

        if call.data == '/login':
            print('Login')


bot.infinity_polling()
