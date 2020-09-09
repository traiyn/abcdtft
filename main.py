import json
import requests

def main():

    account_names = ['Traiyn', 'PVLeviathan']

    with open('secret.json') as f:
        api_key = json.load(f)

    for name in account_names:
        # Get account info
        resp = requests.get(f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}?api_key={api_key['key']}")
        account_id = resp.json()['accountId']
        # Get match history
        resp = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key['key']}")
        print(resp.text)

if __name__ == '__main__':
    main()