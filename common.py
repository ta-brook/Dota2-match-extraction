import json

def transform_readable_json(file_path, saved_name):
    '''
    import and transformed json to readable format
    '''
    data = json.load(open(file_path, encoding='utf-8'))
    
    with open(saved_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# level by exp
def calculate_level_by_exp(exp):
    if exp < 230:
        level = 1
    elif exp < 600:
        level = 2
    elif exp < 1080:
        level = 3
    elif exp < 1660:
        level = 4
    elif exp < 2260:
        level = 5
    elif exp < 2980:
        level = 6
    elif exp < 3730:
        level = 7
    elif exp < 4620:
        level = 8
    elif exp < 5550:
        level = 9
    elif exp < 6520:
        level = 10
    elif exp < 7530:
        level = 11
    elif exp < 8580:
        level = 12
    elif exp < 9805:
        level = 13
    elif exp < 11055:
        level = 14
    elif exp < 12330:
        level = 15
    elif exp < 13630:
        level = 16
    elif exp < 14955:
        level = 17
    elif exp < 16455:
        level = 18
    elif exp < 18045:
        level = 19
    elif exp < 19645:
        level = 20
    elif exp < 21495:
        level = 21
    elif exp < 23595:
        level = 22
    elif exp < 25945:
        level = 23
    elif exp < 28545:
        level = 24
    elif exp < 32045:
        level = 25
    elif exp < 36545:
        level = 26
    elif exp < 42045:
        level = 27
    elif exp < 48545:
        level = 28
    elif exp < 56045:
        level = 29
    else:
        level = 30

    return level

# transform_readable_json('dumps/heroes.json', 'dumps/heroes_readable.json')