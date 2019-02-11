# -*- coding: utf-8 -*-


class Users :
    def __init__(self) :
        self.base = dict() ##{key: [user_id, params{course: -, stream: -, group: -}], change}
        self.cnt = 0

    def check_cnt(self) :
        if self.cnt >= 1 :
            Users.save_base(self)
        if self.cnt >= 10 :
            Users.send_base(self)
            self.cnt = 0
    
    def delete_user(self, chat_id) :
        Users.add_user(self, chat_id, "-1")
        self.base.pop(chat_id)
   
    def add_user(self, chat_id) :
        if self.base.get(chat_id) is None :
            self.cnt += 1
            self.base[chat_id] = [{"course": None, "stream": None, "group": None}, {"course": None, "stream": None, "group": None}, 1, 1, 0]
            Users.check_cnt(self)
            ##[0] - save; [1] - current
            
    def add_param(self, chat_id, message) :
        Users.add_user(self, chat_id)
        value, param = message.split()
        if param == "курс" :
            param = "course"
        if param == "группа" :
            param = "group"
        if param == "поток" :
            param = "stream"
        self.base[chat_id][1][param] = value
        self.base[chat_id][3] = 0
        #print(chat_id)

    def get_param(self, chat_id, param) :
        index = self.base[chat_id][2]
        return self.base[chat_id][index][param]

    def get_all_params(self, chat_id) :
        params = []
        index = self.base[chat_id][2]
        #print(index)
        #print(self.base[chat_id][index])
        for param in self.base[chat_id][index].keys() :
            #print(param)
            params.append(Users.get_param(self, chat_id, param))
        return params
        
    def save_params(self, chat_id) :
        self.cnt += 1
        self.base[chat_id][3] = 0
        for param in self.base[chat_id][0].keys() :
            self.base[chat_id][0][param] = self.base[chat_id][1][param]
        Users.check_cnt(self)
        
    def reset_save_params(self, chat_id) :
        self.base[chat_id][3] = 0
        self.cnt += 1
        for param in self.base[chat_id][0].keys() :
            self.base[chat_id][0][param] = None
        Users.check_cnt(self)
        
    def on_flag(self, chat_id) :
        self.base[chat_id][2] = 1

    def off_flag(self, chat_id) :
        self.base[chat_id][2] = 0

    def save_base(self) :
        file = open("users.txt", "w")
        for el in self.base.keys() :
            file.write("{" + str(el) + ": " + str(self.base[el]) + "}\n")
        file.close()
        
    def recovery_base(self) :
        self.base = dict()
        file = open("users.txt", "r")
        for el in file :
            el = eval(el)
            for lel in el.keys() :
                self.base[lel] = el[lel]
        #print(self.base, 2)
        file.close()

    def send_base(self) :
        Users.save_base(self)
        return open("users.txt", "r")

    def change_trigger(self, chat_id) :
        if self.base[chat_id][4] == 1 :
            self.base[chat_id][4] = 0
        else :
            self.base[chat_id][4] = 1

    def get_change_trigger(self, chat_id) :
        return self.base[chat_id][4]  
            
##a = Users()
##a.add_user("111")
##a.recovery_base()
##print(a.base)
##print(a.base[111][4])
##a.change_trigger(111)
##print(a.base)
##print(a.base[111][4])
