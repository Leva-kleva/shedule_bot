# -*- coding: utf-8 -*-

import myparser
import telebot
import base_users
import consts_inf
import datetime

def main():  
    token = "717734285:AAEAtWXy_l0Ezj5CFy_h5iUBPaH2MSB0u-8"
    bot = telebot.TeleBot(token)
    users = base_users.Users()
    users.recovery_base()

    @bot.message_handler(commands=["start"])
    def command_start(message) :
        try :
            users.add_user(message.chat.id)
            s = "\nК сожалению, упал сайт с расписанием, поэтому бот частично парализован. Как только сайт восстановят, всё будет работать, а к выходным я поправлю бот, чтобы такого больше не случалось. Извините за неудобства:)"
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start", "/settings")
            keyboard.row("Где у меня ща?")
            keyboard.row("Моё расписание") #
            keyboard.row("Чужое расписание", "Расписание уч. части") 
            keyboard.row("Схема пятого этажа", "Расписание звонков")
            keyboard.row("Обновления", "Обратная связь")
            bot.send_message(message.chat.id, "Start\n" + s, reply_markup = keyboard)   
        except :
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "error. please tap the /start", reply_markup = keyboard)

    @bot.message_handler(commands=["help"])
    def command_help(message) :
        try:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)
        except:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "error. please tap the /start", reply_markup = keyboard)

    @bot.message_handler(commands=["settings"])
    def command_settings(message) :
        try:
            users.off_flag(message.chat.id)
            params = users.get_all_params(message.chat.id)
            bot.send_message(message.chat.id, "курс: {0}\nпоток: {1}\nгруппа: {2}".format(*params))
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start", "Изменить")
            bot.send_message(message.chat.id, "tap Изменить for change setiings.", reply_markup = keyboard)
        except:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "error. please tap the /start", reply_markup = keyboard)

    @bot.message_handler(content_types=["text"])
    def all_messages(message):
        try:
            if message.text == "Моё расписание" or message.text == "Где у меня ща?" :
                if None in users.get_all_params(message.chat.id) :
                    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                    keyboard.row("/start", "/settings")
                    bot.send_message(message.chat.id, "Выполните настройку параметров (/settings)", reply_markup = keyboard)
                else :
                    if message.text == "Моё расписание" :
                        users.off_flag(message.chat.id)
                        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                        keyboard.row("/start")
                        #keybord.row("сегодня", "завтра")
                        keyboard.row("ПН", "ВТ", "СР")
                        keyboard.row("ЧТ", "ПТ", "СБ")
                        bot.send_message(message.chat.id, "Выберите день", reply_markup = keyboard)
                    elif message.text == "Где у меня ща?" :
                        users.off_flag(message.chat.id)
                        params = users.get_all_params(message.chat.id)
                        s = myparser.where(*params)
                        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                        keyboard.row("/start")
                        bot.send_message(message.chat.id, s, reply_markup = keyboard)
                    
            elif message.text == "Изменить" or message.text == "Чужое расписание" :
                #if message.text == "Изменить" :
                    #users.change_trigger(message.chat.id)
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
                #if get_change_trigger(message.chat.id) == 1 :
                keyboard.row("Сохранить настройки")
                #else :
                keyboard.row("ПН", "ВТ", "СР")
                keyboard.row("ЧТ", "ПТ", "СБ")
                bot.send_message(message.chat.id, "Выберите необходимый пункт", reply_markup = keyboard)

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
                bot.send_message(message.chat.id, "Сказать спасибо, выразить пожелания, сообщить об ошибках можно мне: @Leva_kleva", reply_markup = keyboard)

            elif message.text == "Расписание звонков" :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                bot.send_message(message.chat.id, myparser.main_parse(*[None, None, None, 1]), reply_markup = keyboard)

            elif message.text == "Схема пятого этажа" :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                bot.send_photo(message.chat.id, open("shema.jpg", "rb"))
                bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)

            elif message.text == "754698743:AAFC72Z2gqru0fR3xiJVQ95AcqtHB5d7akk" :
                file = users.send_base()
                bot.send_document(260850155, file)

            elif message.text == "Обновления" :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                s = "1) добавлены схема пятого этажа, функция 'где у меня ща?'\n2) исправлены проблемы с хостом. Теперь при падении бота ваши настройки не сбросятся. Бот работает круглосуточно\n3) подправлено отображение расписания\n\nЕсли вы нашли ошибку в своем расписание -- напишите мне @Leva_kleva обязательно\n\nВы всё также можете рассказать о боте своим друзьями и всё также сказать спасибо, выразить свои пожелания, сообщить об ошибках мне @Leva_kleva"
                bot.send_message(message.chat.id, s, reply_markup = keyboard)

            elif message.text == "Расписание уч. части" :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                s = "Часы приема учебной части:\n\n08:45-11:00\n12:00-13:15\n14:15-17:00"
                bot.send_message(message.chat.id, s, reply_markup = keyboard)
                
            else :
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row("/start")
                bot.send_message(message.chat.id, "tap the /start", reply_markup = keyboard)
                
        except:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start")
            bot.send_message(message.chat.id, "error. please tap the /start", reply_markup = keyboard)

    bot.polling(none_stop=True)

if __name__ == '__main__':  
    main()
