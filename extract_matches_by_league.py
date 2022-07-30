import requests
import json
import time

save_path = 'raw_json/'

CREDENTIAL = ''

dota_data = json.load(open('readable_json_TI_key/TI10_matches.json', encoding='utf-8'))
t = time.time()
for i, game in enumerate(dota_data):
    time.sleep(1)
    print(i, game['match_id'])
    URL = f"https://api.opendota.com/api/matches/{game['match_id']}?{CREDENTIAL}"
    r = requests.get(url=URL)
    data = r.json()

    print(type(data))

    with open(f'{save_path+str(game["match_id"])}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# FOR TEST
# heroes
URL = f"https://api.opendota.com/api/heroes"
r = requests.get(url=URL)
data = r.json()
print(data)
print(type(data))

with open('dumps/heroes_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# teams
URL = f"https://api.opendota.com/api/teams"
r = requests.get(url=URL)
data = r.json()
print(data)
print(type(data))

with open('dumps/teams_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

