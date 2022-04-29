import requests
import json
import os
import time
from ratelimit import limits, sleep_and_retry

REGION = "NA"
RATE_LIMIT = {
    'per_second': 20,
    'per_minute': 50
}
API_CALLS = 100
ONE_MINUTE = 120

RIOT_API_URL_BASE = "https://na1.api.riotgames.com/"
RIOT_API_URL_TFT = RIOT_API_URL_BASE + "tft/"

RIOT_API_URL_BASE = "https://na1.api.riotgames.com/"
RIOT_API_URL_TFT = RIOT_API_URL_BASE + "tft/"
RIOT_API_URL_TFTMATCH = "https://americas.api.riotgames.com/tft/match/v1/matches/"
# get Riot API key
with open('secret.json') as f:
    riot_api_key = json.load(f)['riot-key']

@sleep_and_retry
@limits(calls=API_CALLS, period=ONE_MINUTE)
def call_api(url):
    # Need additional error handling for common errors (network error, etc.).
    _response = requests.get(url)
    _status = _response.status_code

    if _status != 200:
        raise Exception('API response: {}'.format(_response.status_code))
    return _response, _status


def get_summoner_id(name):
    # Any additional error handling needed?
    riot_api_url_summoner = RIOT_API_URL_TFT + 'summoner/v1/summoners/by-name/' + name + '?api_key=' + riot_api_key
    resp, stat = call_api(riot_api_url_summoner)
    return resp.json()['puuid']


def get_summoner_match_history(id):
    # Any additional error handling needed?
    riot_api_url_tftmatches = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + id + "/ids?count=1000&api_key=" + riot_api_key
    resp, stat = call_api(riot_api_url_tftmatches)
    return list(resp.json())


def get_summoner_match_data(summ, match_history):

    existing_matches = os.listdir(os.path.join('data', summ))

    for match in match_history:
        match_filename = match + '.json'
        if match_filename in existing_matches:
            continue
            
        request_url = RIOT_API_URL_TFTMATCH + match + '?api_key=' + riot_api_key
        response, status = call_api(request_url)
        # If rate limit reached, we will need to retry. Add back into the queue.
        if status == 429:
            print('Rate limit exceeded. Adding to back of queue to retry.')
            match_history.append(match)
            print('Sleep for 60 seconds.')
            time.sleep(60)
            continue
        match_info = response.json()
        filepath = os.path.join('data', summ, match_filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(match_info, f)