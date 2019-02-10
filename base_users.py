# -*- coding: utf-8 -*-


class Users :
    def __init__(self) :
        self.base = dict() ##{key: [user_id, params{course: -, stream: -, group: -}], change}
        self.cnt = 0

    def check_cnt(self) :
        if self.cnt >= 1 :
            self.cnt = 0
            Users.save_base(self)
    
    def delete_user(self, chat_id) :
        Users.add_user(self, chat_id, "-1")
        self.base.pop(chat_id)
   
    def add_user(self, chat_id) :
        if self.base.get(chat_id) is None :
            self.cnt += 1
            self.base[chat_id] = [{"course": None, "stream": None, "group": None}, {"course": None, "stream": None, "group": None}, 1, 1] 
            Users.check_cnt(self)
            ##[0] - save; [1] - current
            
    def add_param(self, chat_id, message) :
        Users.add_user(self, chat_id)
        value, param = message.split()
        self.base[chat_id][1][param] = value
        self.base[chat_id][3] = 0
        print(chat_id)

    def get_param(self, chat_id, param) :
        index = self.base[chat_id][2]
        return self.base[chat_id][index][param]

    def get_all_params(self, chat_id) :
        params = []
        index = self.base[chat_id][2]
        for param in self.base[chat_id][index].keys() :
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
        file.close()

