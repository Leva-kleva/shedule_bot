import urllib.request
from bs4 import BeautifulSoup

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


def format_shedule(shedule, group, day) :
    fshedule = []
    #print(shedule) 
    days = {"1": "Monday", "2": "Tuesday", "3": "Wednesday",
            "4": "Thursday", "5": "Friday", "6": "Saturday"}
    fshedule.append("Group is " + str(group)) 
    fshedule.append("Day is " + days[str(day)])
    fshedule.append("")
    for i in range(2, len(shedule), 1) :
        tmp = shedule[i][:len(shedule[i])-2]
        if tmp == "\xa0" :
            tmp = "no pair."
        #if len(tmp) == 1 :
            #tmp = "no pair."
        fshedule.append(tmp)
    return fshedule 
    

       
def parse(html, group, day) :
    soup = BeautifulSoup(html)
    table = soup.find("table")
    nomber_group = search_nomber_group(table.find("tr", class_="tdheader"), group)
    rows = table.find_all("tr")
    shedule = get_shedule(rows, nomber_group, day)
    shedule = format_shedule(shedule, group, day)
    return shedule
    

def main_parse(course, stream, group, day) :
    s = ""
    for el in parse(get_html(generate_url(course, stream)), group, day) :
        s += el + '\n'
    #print(s)
    return s




if __name__ == "__main__" :
    args = list(map(int, input().split()))
    #args = [2, 3, 214, 4]
    main_parse(*args) #args = [course, stream, group, day]
