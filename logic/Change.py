import json
from lexicon.Lexicon import weekday_names

def check_day(week:str, reverse: bool = False):
    with open(f'data\\{week}.json', encoding='utf-8') as file:
        dict = json.load(file)

    days = []
    for day, other in dict.items(): # Перебор дней
        days.append(day)
    
    if not reverse:
        return days
    else:
        return [day for day in weekday_names if day not in days]
