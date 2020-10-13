import requests
import json
import os
from api_config import ApiConfig

RANKS = ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND']
DIVISIONS = ['IV','III','II','I']

RATE_LIMIT = {
    'per_second': 20,
    'per_minute': 100
}


def get_summoner():
    pass

def get_summoners_by_league(config, league="DIAMOND", division='I'):
    api_key = config.api_key
    url = f"https://na1.api.riotgames.com/tft/league/v1/entries/{league}/{division}?api_key={api_key}"
    resp = requests.get(url).json()

    filename = league + '_' + division + '.json'
    filepath = os.path.join('data', filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump(resp, f)

with open('secret.json') as f:
    riot_api_key = json.load(f)['riot-key']

riot_api_config = ApiConfig(riot_api_key, RATE_LIMIT)

get_summoners_by_league(riot_api_config, "GOLD", "II")

for rank in RANKS:
    for div in DIVISIONS:
        get_summoners_by_league(riot_api_config, rank, div)

