import json

def register(id: int, name: str, username: str, date: str = None):
    with open(r'data\Users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    if not str(id) in users:
        users[id] = {
            'name': name,
            'username': username,
            'active': True,
            'date': date,
            'settings': {
                'notifications': False,
                'day_block_messages': False,
                'week_block_messages': False
            }
        }
    else:
        users[str(id)]['active'] = True
        users[str(id)]['date'] = date

    with open(r'data\Users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def unregister(id: int, date: str = None):
    with open(r'data\Users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    users[str(id)]['active'] = False
    users[str(id)]['date'] = date

    with open(r'data\Users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def set_settings(id: int, setting: str, choice: bool):
    with open(r'data\Users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    users[str(id)]['settings'][setting] = choice

    with open(r'data\Users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def get_settings(id: int, setting: str):
    with open(r'data\Users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    value = users[str(id)]['settings'][setting]

    return value
