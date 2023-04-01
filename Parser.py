from bs4 import BeautifulSoup
import requests
import datetime
import re
import json

def get_page(url):
    try:
        response = requests.get(url)
    except Exception as e:
        #print(e)
        print('Возможно стоить проверить инет!')
        raise

    if response.status_code != 200:
        print('Ошибка доступа к сайту!')
        raise

    return BeautifulSoup(response.text, 'lxml')


def get_schedule_in_json():
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)

    urls = ['https://www.istu.edu/schedule/?group=464771', f'https://www.istu.edu/schedule/?group=464771&date={str(next_monday)}']

    schedule_dict = {}
    for i, url in enumerate(urls):
        html_page = get_page(url)
        
        content = html_page.find('div', class_='content')
        
        even_odd_week_now = content.find('div', class_='alert-info').find(string=re.compile('неделя')).find_next().text # четная/нечетна

        if even_odd_week_now == 'четная': # --------------Нужно будет поменять на "!=" если исправят ошибку в коде расписания-------------------------
            next_even_odd_week = 'class-even-week'
        else:
            next_even_odd_week = 'class-odd-week'

        day_dict = {}
        days_of_the_week = content.find_all('h3', class_='day-heading') # Список с днями и датами
        for day in days_of_the_week:
            name_date_day = day.text # Дата и название дня недели
            name_day = name_date_day.split(',')[0].strip() # Название дня недели
            date = name_date_day.split(',')[1].strip() # Дата
            
            list_subject = [] # Список предметов для конкретного дня
            pairs = day.find_next().find_all('div', class_='class-line-item') # Список пар разбитых по времени
            for pair in pairs:
                pair_start_time = pair.find('div', class_='class-time').text # Время начала пары

                # subject_dict = {}
                for subject in pair.find_all('div', class_='class-tail'): # Список предметов для конкретного времени
                    if next_even_odd_week in subject['class'] or subject.text == 'свободно':
                        continue
                    else:
                        list_subject.append({
                            'time':pair_start_time,
                            'name_pair':subject.find('div', class_='class-pred').text,
                            'audience':subject.find('div', class_='class-aud').text,
                            'info':subject.find('div', class_='class-info').text.strip()
                            })
                
            day_dict[name_day] = {
                'date':date,
                'pairs':list_subject
                }

        with open(f'{even_odd_week_now}.json', 'w') as f:
            json.dump(day_dict, f, indent=4, ensure_ascii=False) # 


if __name__ == '__main__':
    get_schedule_in_json()