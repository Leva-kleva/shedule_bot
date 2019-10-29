# -*- coding: utf-8 -*-

import telebot
import const_inf
import my_base
from request import Request

def send_main_keyboard(chat_id) :   
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row("Расписание на сегодня", "Моё расписание") #
    keyboard.row("Чужое расписание", "Расписание уч. части") 
    keyboard.row("Схема пятого этажа", "Расписание звонков")
    keyboard.row("/settings", "Обратная связь")
    bot.send_message(chat_id, "Выбери нужный пункт", reply_markup = keyboard)  

        
def main():
    try:
        token = const_inf.token
        global bot
        bot = telebot.TeleBot(token)
        #base = my_base.Base()
        #base.recovery_base()
        
        rqst = Request(bot)
        rqst.recovery_base()
        
        @bot.message_handler(commands=["start"])
        def command_start(message) :
            #obj_user = user.User(message.chat.id)
            rqst.add_user(message.chat.id)
            send_main_keyboard(message.chat.id)
              
              
        @bot.message_handler(commands=["help"])
        def command_help(message) :
            answer = "Помоги себе сам:) \nА если не получилось пиши автору бота @Leva_kelva"
            bot.send_message(message.chat.id, answer)
            send_main_keyboard(message.chat.id)
           
           
        @bot.message_handler(commands=["settings"])
        def command_settings(message) :
            info = eval(str(rqst.get_info(message.chat.id))) ## [0, 1, 2]
            answer = "Курс " + str(info[0]) + "\n" + "Поток " + str(info[1]) + "\nГруппа " + str(info[2])
            bot.send_message(message.chat.id, answer)
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row("/start", "Изменить настройки")
            bot.send_message(message.chat.id, "Нажмите 'Изменить настройки', чтобы изменить настройки.", reply_markup = keyboard)
        
        
        @bot.message_handler(content_types=["text"])
        def all_messages(message):
            #print(rqst.base)
            rqst.add_rqst(message.chat.id, message.text)
            rqst.go()
            
            '''
            if message.text in set([const_inf.rqst_id[3], const_inf.rqst_id[4], const_inf.rqst_id[5]]) :
                if message.text == const_inf.rqst_id[3] :
                    answer = "" ##здесь расписание + инфа о запросе (группа и пр)
                    bot.send_message(message.chat.id, answer)
                    send_main_keyboard(message.chat.id)
                
                if message.text == const_inf.rqst_id[4] : 
                    send_dyas(message.chat.id)
                
                if message.text == const_inf.rqst_id[5] :
                    send_course(message.chat.id)
                    ##нужно формировать очередь запроса
            
            elif message.text == const_inf.rqst_id[6] :
                bot.send_message(message.chat.id, const_inf.ans_id[6])
                send_main_keyboard(message.chat.id)
                
            elif message.text == const_inf.rqst_id[7] :
                send photo
                pass
                
            elif message.text == const_inf.rqst_id[8] :
                bot.send_message(message.chat.id, const_inf.ans_id[8])
                send_main_keyboard(message.chat.id)'''
        while True:
            try:
                bot.polling(none_stop=True)
            except:
                pass
    except:
        pass

        
        
if __name__ == '__main__':  
    main()
        