#!/bin/bash

# ==============================================================
# Author: Tim-Mer (https://github.com/Tim-Mer)
# ==============================================================
# Inputs: JSON (Uses the first *_games.json file it finds,
#               avoiding redownloading the file multiple times)
#         DEBUG (Useful for debugging the script in VSCode)
#         HIDE  Don't display sensitive info to terminal
# ==============================================================

API_KEY_TXT=steam_api_key.txt
STEAM_ID_TXT=steam_id.txt
VENV_NAME=venv
PY_SCRIPT=random_steam_game.py
STEAM_DB=steam_db.json

if [[ $@ =~ "DEBUG" ]]; then
    DEBUG_LINE="-m debugpy --listen 0.0.0.0:5678 --wait-for-client"
else
    DEBUG_LINE=""
fi

if [[ $@ =~ "JSON" ]]; then
    JSON_FILE="--steam-id-json `find -name '*_games.json' | head -n 1`"
else
    JSON_FILE=""
fi

if [[ ! -e ${API_KEY_TXT} ]]; then
    echo "INFO: This flow requires a ${API_KEY_TXT} file, lets generate it"
    echo "INFO: You can get an api key here: https://steamcommunity.com/dev "
    echo "Please input you steam api key:"
    read API_KEY
    echo "Printing key: ${API_KEY} to ${API_KEY_TXT}"
    echo "${API_KEY}" > ${API_KEY_TXT}
fi

if [[ ! -e ${STEAM_ID_TXT} ]]; then
    echo "INFO: This flow requires a ${STEAM_ID_TXT} file, lets generate it"
    echo "INFO: You can find your SteamID here: https://www.steamidfinder.com/ "
    echo "Please input the steam id you'd like to use:"
    read STEAM_ID
    echo "Printing key: ${STEAM_ID} to ${STEAM_ID_TXT}"
    echo "${STEAM_ID}" > ${STEAM_ID_TXT}
fi

if [[ ! -e venv ]]; then
    python3 -m venv ${VENV_NAME}
    source ${VENV_NAME}/bin/activate
    python3 -m pip install -r requirements.txt
    if [[ $@ =~ "DEBUG" ]]; then
        python3 -m pip install debugpy
    fi
else
    source ${VENV_NAME}/bin/activate
fi
if [[ ! -e ${STEAM_DB} ]]; then
    echo "INFO: Downloading the steam appid list"
    wget https://api.steampowered.com/ISteamApps/GetAppList/v2/ -O ${STEAM_DB}
fi
CMD="python3 ${DEBUG_LINE} ${PY_SCRIPT} --steam-db ${STEAM_DB} --api-key-file ${API_KEY_TXT} --steam-id `cat ${STEAM_ID_TXT}` ${JSON_FILE}"
if [[ ! $@ =~ HIDE ]]; then
    echo "INFO: Running ${CMD}"
fi
${CMD}
deactivate