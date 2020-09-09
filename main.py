import json
import requests

ACCOUNT_ID = 'NExH5gkVThJbxHhhfOLxh-82Zwc_ONAV6hmOjbk25y_S2UM'

def main():

    account_names = ['Traiyn', 'PVLeviathan']

    with open('secret.json') as f:
        api_key = json.load(f)

    for name in account_names:

    resp = requests.get(f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/Traiyn?api_key={api_key['key']}")
    # resp = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{ACCOUNT_ID}?api_key={api_key['key']}")

    print(resp.text)

if __name__ == '__main__':
    main()