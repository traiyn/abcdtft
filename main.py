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

SUMMONER = "Traiyn"

def main():

    # summoner = input("Please enter a summoner's name: ")
    puuid = riot_api.get_summoner_id(SUMMONER)
    match_history = riot_api.get_summoner_match_history(puuid)
    # Get all match data and save to json files
    riot_api.get_summoner_match_data(SUMMONER, match_history)


if __name__ == '__main__':
    main()