import json
import requests

ACCOUNT_ID = 'NExH5gkVThJbxHhhfOLxh-82Zwc_ONAV6hmOjbk25y_S2UM'

def main():

    with open('secret.json') as f:
        api_key = json.load(f)
    # resp = requests.get('https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/Traiyn?api_key=RGAPI-a6a97a8a-bacd-47ff-a5bb-f42ba6c551a6')
    # resp = requests.get('https://na1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=RGAPI-a6a97a8a-bacd-47ff-a5bb-f42ba6c551a6')
    # resp = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Traiyn?api_key=RGAPI-a6a97a8a-bacd-47ff-a5bb-f42ba6c551a6')
    resp = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{ACCOUNT_ID}?api_key={api_key['key']}")

    print(resp.text)

if __name__ == '__main__':
    main()