import pandas as pd

# let's try traditional way pandas
df_match_info = pd.DataFrame(columns=[
                                    'match_id',
                                    'dire_team_id',
                                    'radiant_team_id',
                                    'start_time',
                                    'duration',
                                    'radiant_score',
                                    'dire_score',
                                    'first_blood_time',
                                    'first_blood_team', # feature eng
                                    'league_id',
                                    'team_win', # feature eng
                                    ])

df_heroes_picked = pd.DataFrame(columns=[
                                    'match_id',
                                    'player_0',
                                    'player_1',
                                    'player_2',
                                    'player_3',
                                    'player_4',
                                    'player_5',
                                    'player_6',
                                    'player_7',
                                    'player_8',
                                    'player_9',
                                    ])

df_players_overall_stat = pd.DataFrame(columns=[
                                    'match_id',
                                    'team_id',
                                    'players',
                                    'kills',
                                    'deaths',
                                    'assists',
                                    'kda',
                                    'level',
                                    'total_gold',
                                    'total_exp',
                                    'net_worth',
                                    'level',
                                    'gpm',
                                    'xpm',
                                    'team_fight_participant'
                                    ])

df_team_overall_stat = pd.DataFrame(columns=[
                                    'match_id',
                                    'radiant_score',
                                    'dire_score'
                                    ])


df_per_minute_data = pd.DataFrame(columns=[
                                    'match_id',
                                    'players',
                                    'time',
                                    'gold_t',
                                    'exp_t',
                                    'lh_t',
                                    'dn_t'
                                    ])

# TODO not done
df_kill_log = pd.DataFrame(columns=[
                                'match_id',
                                'player_kill',
                                'player_killed',
                                'time'
                                ])

df_word_counts = pd.DataFrame(columns=[
                            'match_id',
                            'hf',
                            'gl',
                            'glhf',
                            'gg',
                            'wp'
                            ])

df_heroes = pd.DataFrame(columns=[
                            'hero_id',
                            'name',
                            'localized_name',
                            'primary_attr',
                            'attack_type',
                            'roles',
                            'legs'
                            ])

df_teams = pd.DataFrame(columns=[
                            'team_id',
                            'name',
                            'tag',
                            'win',
                            'lose'
                            ])

df_spec_time = pd.DataFrame(columns=[
                                    'match_id',
                                    'teams',
                                    'total_kills_5_mins',
                                    'total_deaths_5_mins',
                                    'total_kills_10_mins',
                                    'total_deaths_10_mins',
                                    'total_kills_15_mins',
                                    'total_deaths_15_mins',
                                    'total_kills',
                                    'total_deaths',
                                    'total_gold',
                                    'total_exp',
                                    'team_avg_level'
                                    ])

df_adv = pd.DataFrame(columns=[
                            'match_id',
                            'gold_adv',
                            'exp_adv',
                            'time'
                            ])

df_meta_and_counter = pd.DataFrame(columns=[
                                    'match_id',
                                    'teams',
                                    'countered_heroes',
                                    'meta_score'    
                                    ])