from bs4 import BeautifulSoup
import requests
import datetime
import re
import json

def get_page(url):
    """
    url: ссылка на на страницу с расписанием
    """
    try:
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'ru-RU,ru;q=0.9',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
    except:
        print('Возможно стоить проверить инет!')
        raise

    if response.status_code != 200:
        print('Ошибка доступа к сайту!')
        raise

    return BeautifulSoup(response.text, 'lxml')


def get_schedule_in_json():
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)

    urls = {'current_week':'http://www.istu.edu/schedule/?group=464771', 'next_week':f'http://www.istu.edu/schedule/?group=464771&date={str(next_monday)}'}

    for key, url in urls.items():
        html_page = get_page(url)
        
        content = html_page.find('div', class_='content')
        
        # четная/нечетна
        # --------------Нужно будет поменять на "!=" если исправят ошибку в коде расписания-------------------------
        if content.find('div', class_='alert-info').find(string=re.compile('неделя')).find_next().text == 'четная':
            next_even_odd_week = 'class-even-week'
        else:
            next_even_odd_week = 'class-odd-week'

        day_dict = {}
        for day in content.find_all('h3', class_='day-heading'): # Список с днями и датами
            # name_date_day = day.text # Дата и название дня недели
            name_day = day.text.split(',')[0].strip() # Название дня недели
            date = day.text.split(',')[1].strip() # Дата
            
            list_subject = [] # Список предметов для конкретного дня
            for pair in day.find_next().find_all('div', class_='class-line-item'): # Список пар разбитых по времени
                pair_start_time = pair.find('div', class_='class-time').text # Время начала пары

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

        with open(f'{key}.json', 'w', encoding='utf-8') as f:
            json.dump(day_dict, f, indent=4, ensure_ascii=False)


def load_json(week: str, name_day: str = ''):
    """
    week: название json файла с расписанием "current_week"/"next_week"
    name_day: название дня недели (необязательный параметр)
    """

    with open(f'{week}.json', encoding='utf-8') as file:
        dict = json.load(file)
    
    list = []
    for day, other in dict.items(): # Перебор дней
        list.append([])
        if name_day in day:
            list[-1].append(f'<i><b>{day}, {other["date"]}</b></i>')
            for pair in other['pairs']:
                list[-1].append(f'{pair["time"]}\n{pair["name_pair"]}\n<u>{pair["audience"]}</u>\n{pair["info"]}')
        else:
            list.pop()
    
    return list


# if __name__ == '__main__':
    # get_schedule_in_json()