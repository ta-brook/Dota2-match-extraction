from collections import defaultdict
import collections
import pandas as pd
import json
import os

from common import calculate_level_by_exp
from dataframe import df_word_counts
from dataframe import df_heroes
from dataframe import df_kill_log
from dataframe import df_match_info
from dataframe import df_heroes_picked
from dataframe import df_players_overall_stat
from dataframe import df_per_minute_data
from dataframe import df_teams
from dataframe import df_team_overall_stat
from dataframe import df_adv
from dataframe import df_spec_time
from dataframe import df_meta_and_counter

MATCHES_LONGER_25 = 'matches_longer_25/'
MATCHES_NOT_LONGER_25 = 'matches_not_longer_25/'
ALL_MATCHES = 'raw_json/'
DUMP_FOLDER = 'dumps/'
TEST_FOLDER = 'for_test/'
SAVE_FOLDER = 'csv/'

# counter heroes
df_counter = pd.read_csv('csv/hero_counter.csv')
# meta heroes
df_meta = pd.read_csv('csv/meta_hero.csv')

# data = json.load(open(ALL_MATCHES+'6054718020.json', encoding='utf-8'))

# nested dict for keeping heroes data
hero_collection = defaultdict(dict) 

count = 0

heroes = json.load(open(DUMP_FOLDER+'heroes_data.json', encoding='utf-8'))
for hero in heroes:
    # TODO append heroes data in to our nested dict
    hero_collection[hero['id']]['name'] = hero['name']
    hero_collection[hero['id']]['localized_name'] = hero['localized_name']

    df_heroes = df_heroes.append({
                                'hero_id' : hero['id'],
                                'name' : hero['name'],
                                'localized_name' : hero['localized_name'],
                                'primary_attr' : hero['primary_attr'],
                                'attack_type' : hero['attack_type'],
                                'roles' : hero['roles'],
                                'legs' : hero['legs']
                                },
                                ignore_index=True)
print('hero id done')

teams = json.load(open(DUMP_FOLDER+'teams_data.json', encoding='utf-8'))
for team in teams:
    df_teams = df_teams.append({
                                'team_id' : team['team_id'],
                                'name' : team['name'],
                                'tag' : team['tag'],
                                'win' : team['wins'],
                                'lose' : team['losses']
                                },
                                ignore_index=True)
print('teams id done')

# test TEST_FOLDER
# real ALL_MATCHES

for file in os.listdir(ALL_MATCHES):
    data = json.load(open(ALL_MATCHES+file, encoding='utf-8'))
    
    print(f'loop number: {count} \n matche id: {data["match_id"]}')
    if data['radiant_win']:
        winner = 'radiant'
    else:
        winner = 'dire'
    
    # create dict for every player picked hero both id and name (for each game)
    players_hero_id = defaultdict(dict)
    players_hero_name = defaultdict(dict)
    players_hero_localized_name = defaultdict(dict)
    players_hero_name_swapped = defaultdict(dict)
    players_localized_name_swapped = defaultdict(dict)
    # events log
    kill_log = defaultdict(dict) # key: time, value: 'killerId_kill_killedId'

    for idx in range(10):
        players_hero_id[idx] = data['players'][idx]['hero_id']
    
    for idx, hero_id in enumerate(players_hero_id.values()):  
        players_hero_name[idx] = hero_collection[hero_id]['name'] # maybe somehow we might need it
        players_hero_localized_name[idx] = hero_collection[hero_id]['localized_name']
    
    # swap those key and value for df_kill_log
    for key, value in players_hero_name.items():
        players_hero_name_swapped[value] = key
    
    # TODO 
    for key, value in players_hero_localized_name.items():
        players_localized_name_swapped[value] = key
    # print(df_counter)
    # print(players_localized_name_swapped)

    # count counter hero on enemy teams
    radiant_countered = 0
    dire_countered = 0
    for idx in range(10):
        for index, row in df_counter.iterrows():
            if idx <= 4:
                if players_hero_localized_name[idx] == row['localized_name']:
                    enemy_counter = [row["Hero_Counter_1"], row["Hero_Counter_2"], row["Hero_Counter_3"], row["Hero_Counter_4"], row["Hero_Counter_5"], row["Hero_Counter_6"], row["Hero_Counter_7"], row["Hero_Counter_8"], row["Hero_Counter_9"], row["Hero_Counter_10"], row["Hero_Counter_11"], row["Hero_Counter_12"]]
                    for i in range(5):
                        for hero in enemy_counter:
                            if players_hero_localized_name[i+5] == hero:
                                radiant_countered += 1
            else:
                if players_hero_localized_name[idx] == row['localized_name']:
                    enemy_counter = [row["Hero_Counter_1"], row["Hero_Counter_2"], row["Hero_Counter_3"], row["Hero_Counter_4"], row["Hero_Counter_5"], row["Hero_Counter_6"], row["Hero_Counter_7"], row["Hero_Counter_8"], row["Hero_Counter_9"], row["Hero_Counter_10"], row["Hero_Counter_11"], row["Hero_Counter_12"]]
                    for i in range(5):
                        for hero in enemy_counter:
                            if players_hero_localized_name[i+5] == hero:
                                print(hero)
                                dire_countered += 1

    print(radiant_countered, dire_countered)

    # count meta heroes score
    dire_meta = 0
    radiant_meta = 0
    for idx in range(10):
        for index, row in df_meta.iterrows():
            if idx <= 4:
                if players_hero_localized_name[idx] == row['localized_name']:
                    radiant_meta += row['meta_point']
            else:
                if players_hero_localized_name[idx] == row['localized_name']:
                    dire_meta += row['meta_point']
    
    print(radiant_meta, dire_meta)

    # count meta and counter hero
    for team in ['radiant', 'dire']:
        if team == 'radiant':
            df_meta_and_counter = df_meta_and_counter.append({
                                                            'match_id' : data['match_id'],
                                                            'teams' : team,
                                                            'countered_heroes' : radiant_countered,
                                                            'meta_score' : radiant_meta 
                                                            },
                                                            ignore_index=True)
        else:
            df_meta_and_counter = df_meta_and_counter.append({
                                                            'match_id' : data['match_id'],
                                                            'teams' : team,
                                                            'countered_heroes' : dire_countered,
                                                            'meta_score' : dire_meta
                                                            },
                                                            ignore_index=True)

    # get event_log
    for idx in range(10):
        if data['players'][idx]['kills_log']:
            # print(data['players'][idx]['kills_log'])
            for event in data['players'][idx]['kills_log']:
                # event: {'time': 316, 'key': 'npc_dota_hero_juggernaut'} (for each)
                kill_log[event['time']] = f'{idx}_kill_{players_hero_name_swapped[event["key"]]}'

    

    # we already got event log now we sort by key (time [m])
    sorted_log = collections.OrderedDict(sorted(kill_log.items()))

    # count total_kill & total_deaths
    radiant_total_kill = 0
    radiant_total_death = 0
    radiant_total_gold = 0
    radiant_total_exp = 0
    radiant_average_level = 0

    dire_total_gold = 0
    dire_total_exp = 0
    dire_average_level = 0

    radiant_exp_lst = []
    dire_exp_lst = []
    print(sorted_log)
    #get kill by time
    radiant_5_mins_kill = 0
    radiant_10_mins_kill = 0
    radiant_15_mins_kill = 0
    dire_5_mins_kill = 0
    dire_10_mins_kill = 0
    dire_15_mins_kill = 0

    if sorted_log:
        for key, value in sorted_log.items():
            if key <= 5*60:
                if int(value[0]) <= 4:
                    radiant_5_mins_kill += 1
                else:
                    dire_5_mins_kill += 1

            elif key <= 10*60:
                if int(value[0]) <= 4:
                    radiant_10_mins_kill += 1
                else:
                    dire_10_mins_kill += 1

            elif key <= 15*60:
                if int(value[0]) <= 4:
                    radiant_15_mins_kill += 1
                else:
                    dire_15_mins_kill += 1

            if key <= 20*60:
                if int(value[0]) <= 4:
                    radiant_total_kill += 1
                else:
                    radiant_total_death += 1
            

    if data['players'][idx]['gold_t'] and len(data['players'][idx]['gold_t']) > 25:
        for idx in range(10):
            for time in range(len(data['players'][idx]['gold_t'])):
                if time == 20:
                    if idx <= 4:
                        radiant_total_gold += data['players'][idx]['gold_t'][time]
                        radiant_total_exp += data['players'][idx]['xp_t'][time]
                        radiant_exp_lst.append(data['players'][idx]['xp_t'][time])
                    else:
                        dire_total_exp += data['players'][idx]['gold_t'][time]
                        dire_total_gold += data['players'][idx]['xp_t'][time]
                        dire_exp_lst.append(data['players'][idx]['xp_t'][time])

        avg_exp_radiant = sum(radiant_exp_lst) / len(radiant_exp_lst)
        avg_exp_dire = sum(dire_exp_lst) / len(radiant_exp_lst)

        dire_average_level = calculate_level_by_exp(avg_exp_radiant)
        radiant_average_level = calculate_level_by_exp(avg_exp_dire)

    else:
        dire_average_level = None
        radiant_average_level = None
        radiant_total_gold = None
        radiant_total_exp = None
        dire_total_gold = None
        dire_total_exp = None


    for team in ['radiant', 'dire']:
        if team == 'radiant':
            df_spec_time = df_spec_time.append({
                                            'match_id' : data['match_id'],
                                            'teams' : team,
                                            'total_kills_5_mins' : radiant_5_mins_kill,
                                            'total_deaths_5_mins' : dire_5_mins_kill,
                                            'total_kills_10_mins' : radiant_10_mins_kill,
                                            'total_deaths_10_mins' : dire_10_mins_kill,
                                            'total_kills_15_mins' : radiant_15_mins_kill,
                                            'total_deaths_15_mins' : dire_15_mins_kill,
                                            'total_kills' : radiant_total_kill,
                                            'total_deaths' : radiant_total_death,
                                            'total_gold' : radiant_total_gold,
                                            'total_exp' : radiant_total_exp,
                                            'team_avg_level' : radiant_average_level
                                            },
                                            ignore_index=True)
        else:
            df_spec_time = df_spec_time.append({
                                            'match_id' : data['match_id'],
                                            'teams' : team,
                                            'total_kills_5_mins' : dire_5_mins_kill,
                                            'total_deaths_5_mins' : radiant_5_mins_kill,
                                            'total_kills_10_mins' : dire_10_mins_kill,
                                            'total_deaths_10_mins' : radiant_10_mins_kill,
                                            'total_kills_15_mins' : dire_15_mins_kill,
                                            'total_deaths_15_mins' : radiant_15_mins_kill,
                                            'total_kills' : radiant_total_death,
                                            'total_deaths' : radiant_total_kill,
                                            'total_gold' : dire_total_gold,
                                            'total_exp' : dire_total_exp,
                                            'team_avg_level' : dire_average_level
                                            },
                                            ignore_index=True)

    # print(dire_average_level)
    # print(players_hero_id)
    # print(players_hero_name)
    # print(players_hero_name_swapped)
    # print(kill_log)
    # print(sorted_log)
    # print(list(sorted_log.keys())[0])

    df_match_info = df_match_info.append({
                                        'match_id' : data['match_id'],
                                        'dire_team_id' : data['dire_team_id'],
                                        'radiant_team_id' : data['radiant_team_id'],
                                        'start_time' : data['start_time'],
                                        'duration' : data['duration'],
                                        'radiant_score' : data['radiant_score'],
                                        'dire_score' : data['dire_score'],
                                        'first_blood_time' : list(sorted_log.keys())[0] if sorted_log else None,
                                        'first_blood_team' : ('radiant' if int(list(sorted_log.values())[0][0]) <= 4 else 'dire') if sorted_log else None, 
                                        'league_id' : data['league']['leagueid'],
                                        'team_win' : winner
                                        },
                                        ignore_index=True)

    if data['radiant_gold_adv']:
        for time in range(len(data['radiant_gold_adv'])):
            df_adv = df_adv.append({
                                'match_id' : data['match_id'],
                                'gold_adv' : data['radiant_gold_adv'][time],
                                'exp_adv' : data['radiant_xp_adv'][time],
                                'time' : time 
                                },
                                ignore_index=True)

    df_heroes_picked = df_heroes_picked.append({
                                        'match_id' : data['match_id'],
                                        'player_0' : data['players'][0]['hero_id'],
                                        'player_1' : data['players'][1]['hero_id'],
                                        'player_2' : data['players'][2]['hero_id'],
                                        'player_3' : data['players'][3]['hero_id'],
                                        'player_4' : data['players'][4]['hero_id'],
                                        'player_5' : data['players'][5]['hero_id'],
                                        'player_6' : data['players'][6]['hero_id'],
                                        'player_7' : data['players'][7]['hero_id'],
                                        'player_8' : data['players'][8]['hero_id'],
                                        'player_9' : data['players'][9]['hero_id'],
                                        }, 
                                        ignore_index=True)

    df_team_overall_stat = df_team_overall_stat.append({
                                                'match_id' : data['match_id'],
                                                'radiant_score' : data['radiant_score'],
                                                'dire_score' : data['dire_score'],
                                                },
                                                ignore_index=True)

    # TODO not done
    try:
        df_word_counts = df_word_counts.append({
                                                'match_id' : data['match_id'],
                                                'hf' : data['all_word_counts']['hf'],
                                                'gl' : data['all_word_counts']['gl'],
                                                'glhf' : data['all_word_counts']['glhf'],
                                                'gg' : data['all_word_counts']['gg'],
                                                'wp' : data['all_word_counts']['wp'],
                                                },
                                                ignore_index=True)
    except:
        print('some word not found')

    if sorted_log:
        for key, value in sorted_log.items():
            # print(key, value)
            # print(value[0], value[-1])
            df_kill_log = df_kill_log.append({
                                            'match_id' : data['match_id'],
                                            'player_kill' : value[0],
                                            'player_killed' : value[-1],
                                            'time' : key
                                            },
                                            ignore_index=True)




    for idx in range(10):
        # print(data['players'][idx]['gold_t'])
        # print(data['match_id'])
        if data['players'][idx]['gold_t'] == None:
            df_per_minute_data = df_per_minute_data.append({
                                                'match_id' : data['match_id'],
                                                'players' : idx,
                                                'time' : None,
                                                'gold_t' : None,
                                                'exp_t' : None,
                                                'lh_t' : None,
                                                'dn_t' : None        
                                                },
                                                ignore_index=True)
        else:
            for time in range(len(data['players'][idx]['gold_t'])):
                df_per_minute_data = df_per_minute_data.append({
                                                    'match_id' : data['match_id'],
                                                    'players' : idx,
                                                    'time' : time,
                                                    'gold_t' : data['players'][idx]['gold_t'][time],
                                                    'exp_t' : data['players'][idx]['xp_t'][time],
                                                    'lh_t' : data['players'][idx]['lh_t'][time],
                                                    'dn_t' : data['players'][idx]['dn_t'][time]        
                                                    },
                                                    ignore_index=True)   

    for side in ['radiant', 'dire']:
        if side == 'radiant':
            for idx in range(5):                                 
                df_players_overall_stat = df_players_overall_stat.append({
                                                    'match_id' : data['match_id'],
                                                    'team_id' : data['radiant_team']['team_id'],
                                                    'players' : idx,
                                                    'kills' : data['players'][idx]['kills'],
                                                    'deaths' : data['players'][idx]['deaths'],
                                                    'assists' : data['players'][idx]['assists'],
                                                    'kda' : data['players'][idx]['kda'],
                                                    'level' : data['players'][idx]['level'],
                                                    'total_gold' : data['players'][idx]['total_gold'],
                                                    'total_exp' : data['players'][idx]['total_xp'],
                                                    'net_worth' : data['players'][idx]['net_worth'],
                                                    'level' : data['players'][idx]['level'],
                                                    'gpm' : data['players'][idx]['gold_per_min'],
                                                    'xpm' : data['players'][idx]['xp_per_min'],
                                                    'team_fight_participant' : data['players'][idx]['teamfight_participation']
                                                    },
                                                    ignore_index=True)
        else:
            for idx in range(5):
                df_players_overall_stat = df_players_overall_stat.append({
                                                    'match_id' : data['match_id'],
                                                    'team_id' : data['dire_team']['team_id'],
                                                    'players' : idx+5,
                                                    'kills' : data['players'][idx+5]['kills'],
                                                    'deaths' : data['players'][idx+5]['deaths'],
                                                    'assists' : data['players'][idx+5]['assists'],
                                                    'kda' : data['players'][idx+5]['kda'],
                                                    'level' : data['players'][idx+5]['level'],
                                                    'total_gold' : data['players'][idx+5]['total_gold'],
                                                    'total_exp' : data['players'][idx+5]['total_xp'],
                                                    'net_worth' : data['players'][idx+5]['net_worth'],
                                                    'level' : data['players'][idx+5]['level'],
                                                    'gpm' : data['players'][idx+5]['gold_per_min'],
                                                    'xpm' : data['players'][idx+5]['xp_per_min'],
                                                    'team_fight_participant' : data['players'][idx+5]['teamfight_participation']
                                                    },
                                                    ignore_index=True)
    count += 1

# print(hero_collection)

# df_match_info.to_csv(SAVE_FOLDER+'match_info.csv')
# df_heroes_picked.to_csv(SAVE_FOLDER+'heroes_picked.csv')
# df_players_overall_stat.to_csv(SAVE_FOLDER+'players_overall_stat.csv')
# df_team_overall_stat.to_csv(SAVE_FOLDER+'team_overall_stat.csv')
# df_word_counts.to_csv(SAVE_FOLDER+'word_counts.csv')
# df_heroes.to_csv(SAVE_FOLDER+'heroes_id.csv')
# df_teams.to_csv(SAVE_FOLDER+'teams_id.csv')
# df_per_minute_data.to_csv(SAVE_FOLDER+'per_minute_data.csv')
# df_kill_log.to_csv(SAVE_FOLDER+'kills_log.csv')
# df_adv.to_csv(SAVE_FOLDER+'adv.csv')
df_spec_time.to_csv(SAVE_FOLDER+'20_mins_data.csv')
# df_meta_and_counter.to_csv(SAVE_FOLDER+'team_meta_and_counter.csv')


# df_match_info.to_csv('test_match.csv')
# df_heroes_picked.to_csv('test_hero_pick.csv')
# df_players_overall_stat.to_csv('test_overall_stat.csv')
# df_team_overall_stat.to_csv('test_team.csv')
# df_word_counts.to_csv('test_word.csv')
# df_heroes.to_csv('test_hero_id.csv')
# df_teams.to_csv('test_teams_id.csv')
# df_per_minute_data.to_csv('test_per_minute.csv')
# df_kill_log.to_csv('test_kills_log.csv')

