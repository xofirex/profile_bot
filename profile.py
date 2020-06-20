import telebot
from telebot import types
import config

API_TOKEN = config.token

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, """\
Привет, для начала регистрации введи свое имя)
""")
    bot.register_next_step_handler(msg, process_name_step)


# Записываем имя и просим ввести возраст
def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        if (len(name) >= 2) and (len(name) <= 20):
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.send_message(chat_id, 'Сколько тебе лет?')
            bot.register_next_step_handler(msg, process_age_step)
        else:
            msg = bot.send_message(chat_id, 'Имя должно иметь от 2 до 20 символов')
            bot.register_next_step_handler(msg, process_name_step)

    except Exception as e:
        bot.reply_to(message, 'oooops')


# Записываем возраст и просим выбрать пол
def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.send_message(chat_id, 'Возраст должен быть числом. Сколько тебе лет?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Мужчина', 'Женщина')
        msg = bot.send_message(chat_id, 'Какой у тебя пол?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Записываем пол и показываем меня с выбором информации или настройки
def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Мужчина') or (sex == u'Женщина'):
            user.sex = sex
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Информация обо мне', 'Настройки')
            msg = bot.send_message(chat_id, 'Спасибо, твои данные сохранены', reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Мужчина', 'Женщина')
            msg = bot.send_message(chat_id, 'Некорректные данные, выбери один из 2 вариантов', reply_markup=markup)
            bot.register_next_step_handler(msg, process_sex_step)

    except Exception as e:
        bot.reply_to(message, 'oooops')


# главное меню
def process_info_settings_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = message.text
        if msg == u"Информация обо мне":
            bot.send_message(chat_id,
                             'Имя: ' + user.name + '\n Возраст:' + str(user.age) + '\n Пол:' + user.sex)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Информация обо мне', 'Настройки')
            msg = bot.send_message(chat_id, "Каким будет следующее действие?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
        elif msg == u"Настройки":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Поменять имя', 'Поменять возраст', 'Поменять пол', 'Назад')
            msg = bot.send_message(chat_id, "Что вы хотите сделать?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_settings_step)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Информация обо мне', 'Настройки')
            msg = bot.send_message(chat_id, 'Ошибка, попробуй еще раз', reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


#  меню настроек
def process_settings_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = message.text
        if msg == u"Поменять имя":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад')
            msg = bot.send_message(chat_id, 'Введи новое имя или нажми назад', reply_markup=markup)
            bot.register_next_step_handler(msg, process_change_name_step)
        elif msg == u"Поменять возраст":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад')
            msg = bot.send_message(chat_id, 'Введи новый возраст или нажми назад', reply_markup=markup)
            bot.register_next_step_handler(msg, process_change_age_step)
        elif msg == u"Поменять пол":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Назад', 'Мужчина', 'Женщина')
            msg = bot.send_message(chat_id, 'Выбери новый пол или нажми назад', reply_markup=markup)
            bot.register_next_step_handler(msg, process_change_sex_step)
        elif msg == u"Назад":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Информация обо мне', 'Настройки')
            msg = bot.send_message(chat_id, "Каким будет следующее действие?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Поменять имя', 'Поменять возраст', 'Поменять пол', 'Назад')
            msg = bot.send_message(chat_id, 'Ошибка, попробуй еще раз', reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# смена имени
def process_change_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[chat_id]
        if name == u"Назад":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Поменять имя', 'Поменять возраст', 'Поменять пол', 'Назад')
            msg = bot.send_message(chat_id, "Что вы хотите сделать?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_settings_step)
        else:
            if (len(name) >= 2) and (len(name) <= 20):
                user.name = name
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('Информация обо мне', 'Настройки')
                msg = bot.send_message(chat_id, "Имя успешно изменено. Каким будет следующее действие?",
                                       reply_markup=markup)
                bot.register_next_step_handler(msg, process_info_settings_step)
            else:
                msg = bot.send_message(chat_id, 'Имя должно иметь от 2 до 20 символов')
                bot.register_next_step_handler(msg, process_change_name_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')

    # смена возраста


def process_change_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        user = user_dict[chat_id]
        if age == u"Назад":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Поменять имя', 'Поменять возраст', 'Поменять пол', 'Назад')
            msg = bot.send_message(chat_id, "Что вы хотите сделать?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_settings_step)
        else:
            if not age.isdigit():
                msg = bot.send_message(chat_id, 'Возраст должен быть числом. Сколько тебе лет?')
                bot.register_next_step_handler(msg, process_change_age_step)
                return
            user.age = age
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Информация обо мне', 'Настройки')
            msg = bot.send_message(chat_id, "Возраст успешно изменен. Каким будет следующее действие?",
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_info_settings_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


    # смена пола
def process_change_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if sex == u"Назад":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Поменять имя', 'Поменять возраст', 'Поменять пол', 'Назад')
            msg = bot.send_message(chat_id, "Что вы хотите сделать?", reply_markup=markup)
            bot.register_next_step_handler(msg, process_settings_step)
        else:
            if (sex == u'Мужчина') or (sex == u'Женщина'):
                user.sex = sex
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('Информация обо мне', 'Настройки')
                msg = bot.send_message(chat_id, "Пол успешно изменен. Каким будет следующее действие?",
                                       reply_markup=markup)
                bot.register_next_step_handler(msg, process_info_settings_step)
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('Назад', 'Мужчина', 'Женщина')
                msg = bot.send_message(chat_id, 'Некорректные данные, выбери один из 3 вариантов', reply_markup=markup)
                bot.register_next_step_handler(msg, process_change_sex_step)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'oooops')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
