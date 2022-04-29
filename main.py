import cassiopeia as cass
from cassiopeia import Summoner, Patch
import csv
import json
import os
import pandas as pd
import requests
from api_config import ApiConfig
import riot_api
import time

REGION = "NA"
SUMMONER = "Traiyn"
RATE_LIMIT = {
    'per_second': 20,
    'per_minute': 100
}

RIOT_API_URL_BASE = "https://na1.api.riotgames.com/"
RIOT_API_URL_TFT = RIOT_API_URL_BASE + "tft/"

def get_summoner_info():
    pass


def main():

    # summoner = input("Please enter a summoner's name: ")


    riot_api_config = ApiConfig(riot_api_key, RATE_LIMIT)
    puuid = riot_api.get_summoner_id(riot_api_config, SUMMONER)
    match_history = riot_api.get_summoner_match_history(riot_api_config, puuid)

    # move below to riot_api_py
    riot_api_url_tftmatch = "https://americas.api.riotgames.com/tft/match/v1/matches/"
    existing_matches = os.listdir(os.path.join('data', SUMMONER))
    counter = 0

    for match in match_history:
        match_filename = match + '.json'
        if match_filename in existing_matches:
            continue
        if counter == 99:
            print('Abiding by API rate limits...')
            time.sleep(60) # 100 per minute
            print('Continuing')
            counter = 0
            
        request_url = riot_api_url_tftmatch + match + '?api_key=' + riot_api_config.api_key
        resp = requests.get(request_url)
        match_info = resp.json()
        filename = match + '.json'
        filepath = os.path.join('data', SUMMONER, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(match_info, f)
        counter += 1

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