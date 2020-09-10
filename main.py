import cassiopeia as cass
from cassiopeia import Summoner, Patch
import json
import pandas as pd
import requests

REGION = "NA"

def main():

    with open('secret.json') as f:
        api_key = json.load(f)['key']

    cass.set_riot_api_key(api_key)
    summoner = cass.get_summoner(name="Traiyn", region=REGION)
    match_history = Summoner(name=summoner.name, region=REGION).match_history(begin_time=Patch.from_str("9.1", region=REGION).start)
    # all_champions = cass.Champions(region=REGION)
    # sub_test(api_key)
    print(match_history)

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