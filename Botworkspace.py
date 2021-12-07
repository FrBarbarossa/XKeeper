import telebot
from telebot import types
import Dataworkspace as dw
import pprint

logged = []

bot = telebot.TeleBot('TOKEN')

next_keyboard = types.InlineKeyboardMarkup()
key_next = types.InlineKeyboardButton(text='Инструкция.', callback_data='/info')
key_logout = types.InlineKeyboardButton(text='Выход.', callback_data='/logout')
next_keyboard.add(key_next, key_logout)

keyboard = types.InlineKeyboardMarkup()
key_register = types.InlineKeyboardButton(text='Регистрация', callback_data='/register')
key_login = types.InlineKeyboardButton(text='Вход', callback_data='/login')
keyboard.add(key_login, key_register)


@bot.message_handler(commands=['start', 'help', 'new', 'login'])
def get_command(message):
    if message.text == '/start':
        # print(message.from_user.id, dw.check_auth(int(message.from_user.id)))
        if not dw.check_auth(int(message.from_user.id)):
            bot.send_message(message.from_user.id,
                             text="Добро пожаловать в XKeeper! Наш бот поможет Вам не забывать о гарантийных талонах и не копить ненужную бумагу.",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, 'Вы уже авторизованы в системе', reply_markup=next_keyboard)

    if message.text.startswith('/new'):
        if not dw.check_auth(int(message.from_user.id)):
            temp_data = message.text.split()
            if len(temp_data) == 3:
                name, psw = temp_data[-2], temp_data[-1]
                if dw.insert_user(name, psw):
                    logged.append(message.from_user.id)
                    dw.auth(message.from_user.id, name)
                    bot.send_message(message.from_user.id,
                                     text='Регистрация прошла успешно!\nВ целях безопасности советуем удалить Ваше сообщение, где Вы указали логин и пароль. Обязательно запомните эти данные для входа в аккаунт!',
                                     reply_markup=next_keyboard)
                else:
                    bot.send_message(message.from_user.id,
                                     'Пользователь с таким именем уже существует, попробуйте снова')
            else:
                bot.send_message(message.from_user.id,
                                 'Введите команду с корректными данными в формате: /new LOGIN PASSWORD')
        else:
            bot.send_message(message.from_user.id, text='Вы уже аторизованы в системе.', reply_markup=next_keyboard)

    if message.text.startswith('/login'):
        if dw.check_auth(int(message.from_user.id)) or message.from_user.id in logged:
            bot.send_message(message.from_user.id, text='Вы уже аторизованы в системе.', reply_markup=next_keyboard)
        else:
            temp_data = message.text.split()
            if len(temp_data) == 3:
                name, psw = temp_data[-2], temp_data[-1]
                if dw.login(name, psw):
                    logged.append(message.from_user.id)
                    dw.auth(message.from_user.id, name)
                    bot.send_message(message.from_user.id,
                                     text='Вы вошли в систему, как {}'.format(name), reply_markup=next_keyboard)
                else:
                    bot.send_message(message.from_user.id,
                                     'Неверный логин или пароль')
            else:
                bot.send_message(message.from_user.id,
                                 'Введите команду с корректными данными в формате: /login LOGIN PASSWORD')


@bot.message_handler(content_types=['text', ])
def get_message(message):
    # print(message)
    if message.content_type == 'text':
        if dw.check_auth(int(message.from_user.id)):
            bot.send_message(message.from_user.id, text='Команда не распознана.', reply_markup=next_keyboard)
        else:
            bot.send_message(message.from_user.id, text='Команда не распознана.', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Моя твоя не понимать, давай буквами')


@bot.callback_query_handler(func=lambda call: True)
def catcher(call):
    if call.data:
        if call.data == '/register':
            bot.send_message(call.from_user.id, text='Создайте Вашего пользователя с помощью /new LOGIN PASSWORD')

        if call.data == '/login':
            bot.send_message(call.from_user.id,
                             text='Войдите в систему введя команду в следующем формате: /login LOGIN PASSWORD')

        if call.data == '/info':
            pass

        if call.data == '/logout':
            dw.logout(call.from_user.id)
            if call.from_user.id in logged:
                logged.remove(call.from_user.id)
            bot.send_message(call.from_user.id,
                             text='Вы успешно вышли из системы!', reply_markup=keyboard)
            print('Вылогинься')


bot.infinity_polling()
