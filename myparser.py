# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import time

timing = ["9:00-10:35", "10:50-12:25", "13:30-15:05",
          "15:20-16:55", "17:05-18:40"]

timing_t = ["00:00", "09:00", "10:35", "10:50", "12:25", "13:30", "15:05",
          "15:20", "16:55", "17:05", "18:40", "99:99", "99:99", "99:99"]

days = {"1": "Monday", "2": "Tuesday", "3": "Wednesday",
            "4": "Thursday", "5": "Friday", "6": "Saturday",
            "7": "None"}

days_t = { "Mon": 1,
         "Tue": 2,
         "Wed": 3,
         "Thu": 4,
         "Fri": 5,
         "Sat": 6,
         "Sun": 7
    }

def generate_url(course, stream) :
    url = "http://ras.phys.msu.ru/table/"
    url += str(course) + "/" + str(stream) + ".htm"
    return url
    

def get_html(url) :
    return urllib.request.urlopen(url).read()


def search_nomber_group(line, group) :
    line = line.find_all("b")
    cnt = 0
    for i in range(1, len(line) - 1, 2) :
        cnt += 1
        if line[i].text.find(str(group)) != -1 :
            return cnt
    return None


def get_shedule(rows, nomber_group, day) :
    try:
        flg_search = 0 #count time
        column_cnt = 0
        small_cnt = 0
        shedule = ["kek", "lol"]
        for row in rows :
            columns = row.find_all("td")
            for column in columns :
                for cell in column.find_all("img") :
                    if cell.get("src") == "/img/day" + str(day) + ".gif" :
                        flg_search = max(1, flg_search)
                        #column_cnt -= 1
                if flg_search in [i for i in range(1, 11, 1)] :
                    column_class = column.get("class")
                    if column_class != None :
                        if column_class[0] == "tdtime" :
                            if flg_search % 2 == 1 :
                                column = column.text.split()
                                shedule.append(column[0] + column[-1] + "t0")
                            flg_search += 1
                            column_cnt += 1
                        elif column_class[0][:6] == "tditem" :
                            n = int(column_class[0][6:])
                            while n > 0 :
                                column_cnt += 1
                                if column_cnt - 1  == nomber_group :
                                    shedule.append(column.text + "q0")
                                n -= 1
                        elif column_class[0][:7] == "tdsmall" :
                            n = int(column_class[0][7:])
                            while n > 0 :
                                column_cnt += 1
                                small_cnt += 1
                                if (shedule[-1][-2] == "w" or shedule[-1][-3] == "w") and shedule[-1][-1:] != "0" :
                                    if column_cnt == int(shedule[-1][-1:]) :
                                        shedule.append(column.text + "w0")
                                if shedule[-1][-2] == "t" and column_cnt - 1 == nomber_group :
                                    shedule.append(column.text + "w" + str(small_cnt))
                                n -= 1

            column_cnt = 0
            small_cnt = 0
        return shedule
    except :
        return None

def dict_shedule(shedule) :
    dshedule = dict()
    curr_key = 0
    for el in shedule[2:] :
        if el[:-2] in timing :
            curr_key = el[:-2]
            dshedule[el[:-2]] = []
        else :
            dshedule[curr_key].append(el[:-2])
    return dshedule

def format_shedule(shedule, group, day) :
    dshedule = dict_shedule(shedule)
    fshedule = []
    fshedule.append("Group is " + str(group)) 
    fshedule.append("Day is " + days[str(day)] + "\n")
    for key in timing :
        fshedule.append(key)
        if len(dshedule[key]) == 1 :
            if dshedule[key][0] == "\xa0" :
                    dshedule[key][0] = "no lessons"
            fshedule.append(dshedule[key][0] + "\n")
        else :
            for i in range(len(dshedule[key])) :
                if dshedule[key][i] == "\xa0" :
                    dshedule[key][i] = "no lessons"
                fshedule.append(str(i+1) + ") " + dshedule[key][i])
            fshedule.append("\n")
    return fshedule


##def format_shedule(shedule, group, day) :
##    fshedule = []
##    print(shedule) 
##    days = {"1": "Monday", "2": "Tuesday", "3": "Wednesday",
##            "4": "Thursday", "5": "Friday", "6": "Saturday",
##            "7": "None"}
##    fshedule.append("Group is " + str(group)) 
##    fshedule.append("Day is " + days[str(day)])
##    fshedule.append("")
##    for i in range(2, len(shedule), 1) :
##        if shedule[i] in timing :
##            
##        #tmp = shedule[i][:len(shedule[i])-2]
##        #if tmp == "\xa0" :
##            #tmp = "no pair."
##        #if len(tmp) == 1 :
##            #tmp = "no pair."
##        #fshedule.append(tmp)
##    return fshedule 
    

       
def parse_p(html, group, day) :
    soup = BeautifulSoup(html)
    table = soup.find("table")
    nomber_group = search_nomber_group(table.find("tr", class_="tdheader"), group)
    rows = table.find_all("tr")
    shedule = get_shedule(rows, nomber_group, day)
    return shedule


def parse(html, group, day) :
    shedule = format_shedule(parse_p(html, group, day), group, day) 
    return shedule


def main_parse(course, stream, group, day) :
    s = ""
    for el in parse(get_html(generate_url(course, stream)), group, day) :
        s += el + '\n'
    print(s)
    return s


def time_into_int(time) :
    time = time.split(":")
    return (int(time[0]), int(time[1]))


def find_time(time) :
    time = time_into_int(time)
    for i in range(len(timing_t)) :
        tmp = time_into_int(timing_t[i])
        if time < tmp :
            return i

def where(course, stream, group) :
   # try:
        now = time.ctime().split()
        if days_t[now[0]] == 7 :
            return "Текуща пара: нет пары.\nСледующая пара: нет пары."
        s = ""
        day = days_t[now[0]]
        curr_time = now[3][:-3]
        #curr_time = "23:59"
        i = find_time(curr_time)
        for q in range(i-1, i+3, 1) :
            timing_t[q] = timing_t[q].split(":")
            timing_t[q][0] = int(timing_t[q][0])
            timing_t[q] = str(timing_t[q][0]) + ":" + str(timing_t[q][1])
       # print((timing_t[i-1] + "-" + timing_t[i]) in timing)
        #print((timing_t[i-1] + "-" + timing_t[i]), timing[0])
        flg = 1
        dshedule = (parse_p(get_html(generate_url(course, stream)), group, day))
        dshedule = dict_shedule(dshedule)
        #print(dshedule)
        if (timing_t[i-1] + "-" + timing_t[i]) in timing:
            key = timing_t[i-1] + "-" + timing_t[i]
            #key = key.zfill(11)
            s += "Текущая пара: " + key + " "
            if len(dshedule[key]) == 1 :
                if dshedule[key][0] == "\xa0" :
                    dshedule[key][0] = "no lessons"
                s += dshedule[key][0]
            else :
                for j in range(len(dshedule[key])) :
                    if dshedule[key][j] == "\xa0" :
                        dshedule[key][j] = "no lessons"
                    s += str(ij+1) + ") " + dshedule[key][j] + "\n"
            s += ("\n")
        else :
            s += "Текущая пара: нет пары.\n"
            flg = 0
            
        if (timing_t[i+flg] + "-" + timing_t[i+flg+1]) in timing:
            key = timing_t[i+flg] + "-" + timing_t[i+flg+1]
            #key = key.zfill(11)
            s += "Следующая пара: " + key + " "
            if len(dshedule[key]) == 1 :
                if dshedule[key][0] == "\xa0" :
                    dshedule[key][0] = "no lessons"
                s += dshedule[key][0]
            else :
                for j in range(len(dshedule[key])) :
                    if dshedule[key][j] == "\xa0" :
                        dshedule[key][j] = "no lessons"
                    s += str(ij+1) + ") " + dshedule[key][j] + "\n"
        else :
            s += "Следующая пара: нет пары."
        
        return s
    #except :
        #return "Возникла ошибка. Сообщите о ней мне @Leva_kleva.\n /start" 



if __name__ == "__main__" :
    pass
    #args = list(map(int, input().split()))
    #args = [2, 3, 214, 2]
    #print(where(2, 3, 214))
    #main_parse(*args) #args = [course, stream, group, day]
