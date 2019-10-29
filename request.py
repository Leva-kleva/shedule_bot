# -*- coding: utf-8 -*-

import telebot 
from my_base import Base
import const_inf
from shedule import Shedule

import pytz
import time
from datetime import datetime


class Request(Base) :
    def __init__(self, bot) :
        super().__init__()
        self.queue = {} # id: [command, [params]]
        self.bot = bot
        self.logs = open("logs.txt", "a")
        self.change = dict()
        
        
    def add_log(self, info) :
        self.logs.write(info + "\n")
        self.logs.close()
        self.logs = open("logs.txt", "a")
        
        
    def send_main_keyboard(self, chat_id) :   
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Расписание на сегодня", "Моё расписание") #
        keyboard.row("Чужое расписание", "Расписание уч. части") 
        keyboard.row("Схема пятого этажа", "Расписание звонков")
        keyboard.row("/settings", "Обратная связь")
        self.bot.send_message(chat_id, "Выбери нужный пункт", reply_markup = keyboard)  


    def send_dyas(self, chat_id):
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("ПН", "ВТ", "СР") 
        keyboard.row("ЧТ", "ПТ", "СБ") 
        self.bot.send_message(chat_id, "Выбери день.", reply_markup = keyboard) 
        
        
    def send_course(self, chat_id) :
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row("1 курс", "2 курс") 
        keyboard.row("3 курс", "4 курс")
        keyboard.row("5 курс (1 маг)", "6 курс (2 маг)")    
        self.bot.send_message(chat_id, "Выбери курс", reply_markup = keyboard)


    def send_stream(self, chat_id) :
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        if self.queue[chat_id][1][0] is None :
            keyboard.row("1 поток", "2 поток", "3 поток") 
        else :
            if self.queue[chat_id][1][0] in set(["1", "2"]) :
                keyboard.row("1 поток", "2 поток", "3 поток")
            else :
                keyboard.row("1 поток", "2 поток")
        self.bot.send_message(chat_id, "Выбери поток", reply_markup = keyboard)
       
       
    def send_nomber_group(self, chat_id) :
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        group = const_inf.nomber_group[self.queue[chat_id][1][0]][self.queue[chat_id][1][1]]
        for i in range(0, len(group)) :
            keyboard.row(group[i]+" группа")    
        self.bot.send_message(chat_id, "Выбери группу", reply_markup = keyboard)
        
        
    def add_rqst(self, chat_id, rqst) :
        if rqst == "stoperr" :
            s = 1/0
        if self.queue.get(chat_id) is None :
            self.queue[chat_id] = [rqst, [None, None, None, None], 1]
        else :
            self.queue[chat_id][2] = 1
            if rqst.find("курс") != -1 :
                self.queue[chat_id][1][0] = rqst.split()[0]
            elif rqst.find("поток") != -1 :
                self.queue[chat_id][1][1] = rqst.split()[0]
            elif rqst.find("группа") != -1 :
                self.queue[chat_id][1][2] = rqst.split()[0]
            elif rqst in set(["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "Все дни"]) :
                self.queue[chat_id][1][3] = rqst.split()[0]
                
            if self.queue[chat_id][0] == "Изменить настройки" :
                for i in range(3) :
                    self.base[chat_id][i] = self.queue[chat_id][1][i]
                    
        if rqst == "Изменить настройки" :
            self.base[chat_id] = [None, None, None]
            
        #Request.add_log(self, str(chat_id)+" "+rqst+" "+str(datetime.now(pytz.timezone("Europe/Moscow"))))

            
    def delete_rqst(self, chat_id) :
        self.queue.pop(chat_id)
            
    #####################
    
        
    def shedule_my(self, chat_id, param) :
        if self.base[chat_id][2] is None :
            answer = "У вас не указана группа. Зайдите в /settings -- 'Изменить настройки', чтобы указать свою группу."
            self.bot.send_message(chat_id, answer)
            Request.send_main_keyboard(self, chat_id)
            Request.delete_rqst(self, chat_id)
            
        elif param[3] is None :
            Request.send_dyas(self, chat_id)
        else :
            for i in range(3) :
                param[i] = self.base[chat_id][i]
            #print(param)
            shdl = Shedule(param[0], param[1], param[2], param[3])
            answer = shdl.get()
            self.bot.send_message(chat_id, answer)
            Request.send_main_keyboard(self, chat_id)
            Request.delete_rqst(self, chat_id)

        
        
    def shedule_now(self, chat_id, param) :
        if self.base[chat_id][2] is None :
            answer = "У вас не указана группа. Зайдите в /settings -- 'Изменить настройки', чтобы указать свою группу."
            self.bot.send_message(chat_id, answer)
            Request.send_main_keyboard(self, chat_id)
            Request.delete_rqst(self, chat_id)
        else :
            currernt_datatime = datetime.now(pytz.timezone("Europe/Moscow"))
            tmp = currernt_datatime.strftime("%d %m %Y %H %M %S")
            d, m, Y, H, M, S = tmp.split()
            days = {
                    "0": "ПН", "1": "ВТ", "2": "СР", "3": "ЧТ", "4": "ПТ", "5": "СБ", "6": "ВС"
                    }
            param[3] = days[str(currernt_datatime.weekday())]
            for i in range(3) :
                param[i] = self.base[chat_id][i]
                
            shdl = Shedule(param[0], param[1], param[2], param[3])
            answer = shdl.get_now()
            
            self.bot.send_message(chat_id, answer)
            Request.send_main_keyboard(self, chat_id)
            Request.delete_rqst(self, chat_id)
            
        
    def shedule_alien(self, chat_id, param) :
        for i in range(4) :
            if param[i] is None :
                keyboard = {
                            0: Request.send_course,
                            1: Request.send_stream,
                            2: Request.send_nomber_group,
                            3: Request.send_dyas
                            }
                keyboard[i](self, chat_id)
                break
            elif i == 3 :
                shdl = Shedule(param[0], param[1], param[2], param[3])
                answer = shdl.get()
                self.bot.send_message(chat_id, answer)
                Request.send_main_keyboard(self, chat_id)
                Request.delete_rqst(self, chat_id)
        
        
    def change_setting(self, chat_id, param) :
        keyboard = {
                    0: Request.send_course,
                    1: Request.send_stream,
                    2: Request.send_nomber_group
                    }
        for i in range(3) :
            if self.base[chat_id][i] is None :
                keyboard[i](self, chat_id)
                break
            elif i == 2 :
                #self.change_user_into_file(chat_id)
                Request.change_user_into_file(self)
                self.bot.send_message(chat_id, "Done.\nДанные сохранены")
                Request.send_main_keyboard(self, chat_id)
                Request.delete_rqst(self, chat_id)
            
        
    def shedule_uchebka(self, chat_id, param) :
        answer = "Часы приема учебной части:\n\n08:45-11:00\n12:00-13:15\n14:15-17:00"
        self.bot.send_message(chat_id, answer)
        Request.send_main_keyboard(self, chat_id)
        Request.delete_rqst(self, chat_id)
                
    
    def floor_plan(self, chat_id, param) :
        self.bot.send_photo(chat_id, open("shema.jpg", "rb"))
        Request.send_main_keyboard(self, chat_id)
        Request.delete_rqst(self, chat_id)


    def shedule_bell(self, chat_id, param) :
        answer = "1 пара: 9:00--10:35\n2 пара: 10:50--12:25\n3 пара: 13:30--15:05\n4 пара: 15:20--16:55\n5 пара: 17:05--18:40"
        self.bot.send_message(chat_id, answer)
        Request.send_main_keyboard(self, chat_id)
        Request.delete_rqst(self, chat_id)
        
        
    def feedback(self, chat_id, param) :
        answer = "По всем вопросам, предложениям и найденным неточностям  писать автору: @Leva_kleva"
        self.bot.send_message(chat_id, answer)
        Request.send_main_keyboard(self, chat_id)
        Request.delete_rqst(self, chat_id)
    
        
    def go(self) :
        CMD = {
                "Расписание на сегодня": Request.shedule_now,
                "Моё расписание": Request.shedule_my,
                "Чужое расписание": Request.shedule_alien,
                "Расписание уч. части": Request.shedule_uchebka,
                "Схема пятого этажа": Request.floor_plan,
                "Расписание звонков": Request.shedule_bell,
                "Обратная связь": Request.feedback,
                "Изменить настройки": Request.change_setting
                }
        
        chat_id_list = list(self.queue.keys())
        #print(self.queue)
        for chat_id in chat_id_list : # el = [rq, [param]]
            if self.queue[chat_id][2] == 1 :
                rqst, param = self.queue[chat_id][0], self.queue[chat_id][1]
                if CMD.get(rqst) is None :
                    pass
                else : 
                    self.queue[chat_id][2] = 0
                    CMD[rqst](self, chat_id, param)


if __name__ == '__main__':  
    a = Request()