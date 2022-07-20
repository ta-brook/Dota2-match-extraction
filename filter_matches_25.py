import json
import os



directory = 'raw_json/'
save_directory_l = 'matches_longer_25/'
save_directory_s = 'matches_not_longer_25/'
count_long = 0
count_short = 0
# I need to filter only matches that longer than 25 mins
for file in os.listdir(directory):
    data = json.load(open(directory+file, encoding='utf-8'))
    if data['duration'] > 60*25:
        print(f'{file} is longer than 25 minutes')
        with open(save_directory_l+file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        count_long += 1
    else:
        print(f'{file} is shorter than 25 minutes, which is only {int(data["duration"]) // 60} minutes')
        with open(save_directory_s+file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        count_short += 1

print(count_long) 
print(count_short)








