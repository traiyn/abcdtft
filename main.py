import cassiopeia as cass
from cassiopeia import Summoner, Patch
import csv
import json
import os
import pandas as pd
import requests

REGION = "NA"
# SUMMONER = "PVLeviathan"

def main():

    summoner = input("Please enter a summoner's name: ")
    with open('secret.json') as f:
        api_key = json.load(f)['riot-key']

    cass.set_riot_api_key(api_key)
    summoner = cass.get_summoner(name=summoner, region=REGION)
    match_history = Summoner(name=summoner.name, region=REGION).match_history(begin_time=Patch.from_str("9.1", region=REGION).start)
    match_info_rows = []
    for match in match_history:
        match_info = {}
        match_info['id'] = match.id
        match_info['queue_id'] = match.queue.id
        match_info['patch'] = match.patch
        match_info['creation'] = match.creation
        match_info['champion'] = match.participants[summoner].champion.name
        match_info['win'] = match.participants[summoner].team.win
        match_info['kills'] = match.participants[summoner].stats.kills
        match_info['deaths'] = match.participants[summoner].stats.deaths
        match_info['assists'] = match.participants[summoner].stats.assists
        match_info['kda'] = match.participants[summoner].stats.kda
        match_info_rows.append(match_info)
        
    match_history_df = pd.DataFrame(match_info_rows)
    match_history_df.set_index('id')
    # all_champions = cass.Champions(region=REGION)
    # sub_test(api_key)
    print(match_history_df)

    filename = summoner + '_matchhistory.csv'
    filepath = os.path.join('data', filename)

    match_history_df.to_csv(filepath)
    # with open(filepath, 'w', newline='') as output:
    #     wr = csv.writer(output, quoting=csv.QUOTE_ALL)
    #     wr.writerow(champions_played)

def sub_test(api_key):
    
    account_names = ['Traiyn']

    for name in account_names:
        # Get account info
        resp = requests.get(f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}?api_key={api_key['key']}")
        account_id = resp.json()['accountId']
        puu_id = resp.json()['puuid']
        # Get match history
        resp = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key['key']}")
        # resp = requests.get(f"https://na1.api.riotgames.com/tft/match/v1/matches/by-puuid/{puu_id}?api_key={api_key['key']}")

        with open('data.txt', 'w') as outfile:
            json.dump(resp.json(), outfile)

    with open('champions.json') as f:
        champions = json.load(f)

    champions = champions['data']
    for champ, info in champions.items():
        key = info['key']
        info['key'] = int(key)
    champs_df = pd.DataFrame(champions)
    # champs_df.reindex(['key'])
    champs_df = champs_df.T
    champs_df.rename(columns={"key": "champion"}, inplace=True)
    champs_df['champion'] = champs_df['champion'].astype('int64')

    matches = resp.json()['matches']
    matches_df = pd.DataFrame(matches)

    matches_df.merge(champs_df, how='left', on='champion')
    print(champs_df.head())
    print(matches_df.head())


if __name__ == '__main__':
    main()