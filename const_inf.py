# -*- coding: utf-8 -*-

token = ""
        
rqst_id = { 
            1: "\start", 2: "\help",
            3: "Где у меня ща?", 4: "Моё расписание",
            5: "Чужое расписание", 6: "Расписание уч. части", 
            7: "Схема пятого этажа", 8: "Расписание звонков",
            9: "/settings", 10: "Обратная связь",
            11: "Изменить настройки"
            }

answ_id = {
            6: "Часы приема учебной части:\n\n08:45-11:00\n12:00-13:15\n14:15-17:00",
            8: "1 пара: 9:00-10:35\n2 пара: 10:50-12:25\n3 пара: 13:30-15:05\n4 пара: 15:20-16:55\n5 пара: 17:05-18:40"
            }

nomber_group = {
                "1": {
                        "1": ["101", "102", "103", "104", "105", "106"],
                        "2": ["107", "108", "109", "110", "111", "112"],
                        "3": ["113", "114", "115", "116", "117", "118"]
                        },
                        
                "2": {
                        "1": ["201", "202", "203", "204", "205", "206"],
                        "2": ["207", "208", "209", "210", "211", "212"],
                        "3": ["213", "214", "215", "216", "217", "218"]
                        },
                        
                "3": { 
                        "1": ["301", "302", "303", "304", "305", "306",
                                "307", "308", "309", "311", "312", "313",
                                "314", "318", "335", "338", "340", "341", 
                                "342", "343"],
                        "2":["315", "316", "317", "319", "320", "321", 
                                "322", "323", "324", "325", "326", "327", 
                                "328", "329", "330", "331"]
                        },
                
                "4": {
                        "1": ["401", "402", "403", "404", "405", "406",
                                "407", "408", "409", "411", "412", "413",
                                "414", "418", "435", "438", "440", "441", 
                                "442", "443"],
                        "2":["415", "416", "417", "419", "420", "421", 
                                "422", "423", "424", "425", "426", "427", 
                                "428", "429", "430", "431"]
                        },
                        
                "5": {
                        "1": ["101М", "102М", "103М", "104М", "105М", "106М",
                                "107М", "108М", "109М", "110М", "111М", "112М",
                                "113М", "114М", "118М", "135М", "138М", "140М", "141М",
                                "142М", "143М", "532", "533", "536"],
                        "2": ["115М", "116М",  "116Мв", "117М", "119М", "120М", "121М",
                                "122М", "123М", "124М", "125М", "127М", "127Мв", "128МБ",
                                "129М", "130М", "131М"]
                        },
                        
                "6": {
                        "1": ["201М", "202М", "203М", "204М", "205М", "206М",
                                "207М", "208М", "209М", "210М", "211М", "212М",
                                "213М", "214М", "218М", "235М", "238М", "240М", "241М",
                                "242М", "243М", "632", "633", "636"],
                        "2": ["215М", "216М", "217М", "219М", "220М", "221М",
                                "222М", "223М", "224М", "225М", "227М", "228МБ",
                                "229М", "230М", "231М"]
                        }
                }
