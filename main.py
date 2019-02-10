import myparser
import telebot
import base_users
import consts_inf

def main():  
    token = "717734285:AAEAtWXy_l0Ezj5CFy_h5iUBPaH2MSB0u-8"
    bot = telebot.TeleBot(token)
    users = base_users.Users()
    users.recovery_base()

    @bot.message_handler(commands=["start"])
    def command_start(message) :
        users.add_user(message.chat.id)
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("/start", "/help")
        keyboard.row("Моё расписание")
        keyboard.row("Чужое расписание", "Расписание звонков")
        keyboard.row("/settings", "Обратная связь")
        bot.send_message(message.chat.id, "Go.", reply_markup = keyboard)

    @bot.message_handler(commands=["help"])
    def command_help(message) :
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("/start")
        bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)

    @bot.message_handler(commands=["settings"])
    def command_settings(message) :
        users.off_flag(message.chat.id)
        params = users.get_all_params(message.chat.id)
        bot.send_message(message.chat.id, "курс: {0}\nпоток: {1}\nгруппа: {2}".format(*params))
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("/start", "Изменить")
        bot.send_message(message.chat.id, "tap Изменить for change setiings.", reply_markup = keyboard)
        
    @bot.message_handler(content_types=["text"])
    def all_messages(message): 
        if message.text == "Моё расписание" :
            if None in users.get_all_params(message.chat.id) :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start", "/settings")
                bot.send_message(message.chat.id, "Выполните настройку параметров (/settings)", reply_markup = keyboard)
            else :
                users.off_flag(message.chat.id)
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                keyboard.row("ПН", "ВТ", "СР")
                keyboard.row("ЧТ", "ПТ", "СБ")
                bot.send_message(message.chat.id, "Выберите день", reply_markup = keyboard)
              
        elif message.text == "Изменить" or message.text == "Чужое расписание" :
            #users.reset_save_params(message.chat.id)
            users.on_flag(message.chat.id)
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            keyboard.row("1 курс", "2 курс")
            keyboard.row("3 курс", "4 курс")
            keyboard.row("5 курс", "6 курс")
            bot.send_message(message.chat.id, "Выберите курс", reply_markup = keyboard)

        elif message.text.find("курс") != -1 :
            users.add_param(message.chat.id, message.text)
            n = message.text.split()[0]
            inf = consts_inf.inf[n]
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            for el in inf :
                keyboard.row(str(el[0]) + " группа " + str(el[1]) + " поток")
            bot.send_message(message.chat.id, "Выберите группу", reply_markup = keyboard)

        elif message.text.find("группа") != -1 :
            params = message.text.split()
            
            param_one = params[0] + " " + params[1]
            param_two = params[2] + " " + params[3]
            users.add_param(message.chat.id, param_one)
            users.add_param(message.chat.id, param_two)

            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            keyboard.row("ПН", "ВТ", "СР")
            keyboard.row("ЧТ", "ПТ", "СБ")
            keyboard.row("Сохранить настройки")
            bot.send_message(message.chat.id, "Выберите день", reply_markup = keyboard)

        elif message.text in consts_inf.days.keys() :
            params = users.get_all_params(message.chat.id)
            params.append(consts_inf.days[message.text])
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, myparser.main_parse(*params), reply_markup = keyboard)

        elif message.text == "Сохранить настройки" :
            users.save_params(message.chat.id)
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)

        elif message.text == "Обратная связь" :
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "Просьба сообщить о пожеланиях к боту и найденных ошибках мне @Leva_kleva", reply_markup = keyboard)

        elif message.text == "Расписание звонков" :
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, myparser.main_parse(*[None, None, None, 1]), reply_markup = keyboard)

        else :
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)

    bot.polling(none_stop=True)

if __name__ == '__main__':  
    main()
