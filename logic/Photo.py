import json

desktop = 'desktop'
statham = 'statham'
today = 'today'


def get_photo(name_photo):
    with open(r'data\photo.json', 'r', encoding='utf-8') as file:
        photos = json.load(file)
    return photos[name_photo]

def set_photo(name_photo, id_photo):
    with open(r'data\photo.json', 'r', encoding='utf-8') as file:
        photos = json.load(file)
    
    photos[name_photo] = id_photo

    with open(r'data\photo.json', 'r', encoding='utf-8') as file:
        json.dump(photos, file, indent=4, ensure_ascii=False)

