import json

# x = open('response.json')
dota_data = json.load(open('readable_json/TI10_matches.json', encoding='utf-8'))

print(json.dumps(dota_data, indent=4, sort_keys=True))

with open('ddddd.json', 'w', encoding='utf-8') as f:
    json.dump(dota_data, f, ensure_ascii=False, indent=4)

print(len(dota_data))

# for i in dota_data:
#     print(i)
    
# plt.show()




# dota_data = json.load(open('response.json', encoding='utf-8'))


# dota_data = json.load(open('league_id.json', encoding='utf-8'))

# print(json.dumps(dota_data, indent=4, sort_keys=True))

# with open('leagued_id_readble.json', 'w', encoding='utf-8') as f:
#     json.dump(dota_data, f, ensure_ascii=False, indent=4)

