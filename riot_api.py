import requests
import json

with open('secret.json') as f:
    riot_api_key = json.load(f)['riot-key']

RIOT_API_URL_BASE = "https://na1.api.riotgames.com/"
RIOT_API_URL_TFT = RIOT_API_URL_BASE + "tft/"

def get_summoner_id(name):
    riot_api_url_summoner = RIOT_API_URL_TFT + 'summoner/v1/summoners/by-name/' + name + '?api_key=' + riot_api_key
    resp = requests.get(riot_api_url_summoner)
    return resp.json()['puuid']


def get_summoner_match_history(id):
    riot_api_url_tftmatches = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + id + "/ids?count=1000&api_key=" + riot_api_key
    resp = requests.get(riot_api_url_tftmatches)
    match_history = list(resp.json())