# -*- coding: utf-8 -*-



class Base:
    def __init__(self) :
        self.base = dict()  ## {id: [inf], id: [inf], ...}
        self.file = open("users.txt", "a")
        
        
    def add_into_file(self, chat_id, info) :
        self.file.write("{" + str(chat_id) + ": " + str(info) + "}\n")
        self.file.close()
        self.file = open("users.txt", "a")
        
        
    def add_user(self, chat_id) :
        if self.base.get(chat_id) is None :
            self.base[chat_id] = [None, None, None]
            Base.add_into_file(self, chat_id, [None, None, None])
        else :
            pass
            
    
    def change_user_into_file(self) :
        self.file.close()
        self.file = open("users.txt", "w")
        for usr in list(self.base.keys()) :
            Base.add_into_file(self, usr, self.base[usr])
        self.file.close()
        self.file = open("users.txt", "a")

        
    def get_info(self, chat_id) :
        return str(self.base[chat_id])

        
    def recovery_base(self) :
        self.base = dict()
        self.file.close()
        self.file = open("users.txt", "r")
        for el in self.file :
            el = eval(el)
            for lel in el.keys() :
                self.base[lel] = el[lel]
        self.file.close()
        self.file = open("users.txt", "a")
        
