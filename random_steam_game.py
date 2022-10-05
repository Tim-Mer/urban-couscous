#!/usr/bin/python3

# ==============================================================
# Author: Tim-Mer (https://github.com/Tim-Mer)
# ==============================================================
# Inputs: --api-key-file  Path to text file with your steam api key
#         --api-key       Your steam api key
#         --steam-id      The steamID you wish to look up a random game for
#         --steam-id-json Parse a pre-downloaded steamID json file')
#         --time-played   Search for game with less than this time played
#                        (In minutes)
#         --steam-db      List of appids with names
# ==============================================================

import argparse
from math import inf
from os import chown
import requests
import json
import random

def main(api_key, steam_id, steam_id_json, steam_db, time_played):
    chosen_game=0
    if not bool(steam_id_json):
        URL="https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + api_key + "&steamid=" + steam_id + "&format=json"
        response = requests.get(URL)
        steam_id_json=steam_id + "_games.json"
        open(steam_id_json, "wb").write(response.content)
        
    with open(steam_id_json, "r") as json_file:
        json_data=json.load(json_file)
        num_games=json_data['response']['game_count']
        print ("Wow you have " + str(num_games) + " games!!!")
        while chosen_game == 0:
            game_no=random.randint(0, num_games-1)
            if json_data['response']['games'][game_no]['playtime_forever'] <= time_played:
                chosen_game=json_data['response']['games'][game_no]['appid']
    chosen_game_name=0
    with open(steam_db, 'r') as steam_db_json:
        steam_db_data=json.load(steam_db_json)
        for appids in steam_db_data['applist']['apps']: 
            if appids['appid'] == chosen_game:
                chosen_game_name=appids['name']
    if chosen_game_name == 0:
        print("ERROR: Something went wrong and it could not find a game for appid: " + str(chosen_game))
        print("You could try rerunning the script or debug this yourself ;)")
        print("Or look it up here: https://steamdb.info/apps/")
    else:
        print("RESULT: " + chosen_game_name)

parser = argparse.ArgumentParser(description='This picks a random steam game that you own from you library and displays it (Try running via `source run.sh`)')
parser.add_argument('--api-key-file', required=False,
                    help='Path to text file with your steam api key')
parser.add_argument('--api-key', required=False,
                    help='Your steam api key')
parser.add_argument('--steam-id', required=True,
                    help='The steamID you wish to look up a random game for')
parser.add_argument('--steam-id-json', required=False,
                    help='Parse a pre-downloaded steamID json file')
parser.add_argument('--time-played', required=False,
                    help='Search for game with less than this time played (In minutes)')
parser.add_argument('--steam-db', required=True,
                    help='List of appids with names')

args = parser.parse_args()
if bool(args.api_key_file):
    with open(args.api_key_file, "r") as key_file:
        api_key=key_file.readline().replace("\n", "")
elif bool(args.api_key):
    api_key=args.api_key
else:
    print("ERROR: No steam api key provided, please check --help and try again!")
    exit
if bool(args.time_played):
    time_played=args.time_played
else:
    time_played=inf
main(api_key, args.steam_id, args.steam_id_json, args.steam_db, time_played)
