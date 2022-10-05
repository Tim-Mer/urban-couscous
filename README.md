# Random Steam Game Picker

This was written mostly to see how to use the steam web API but feel free to use/learn from

## How to use
Requirements: Linux(Any)(I use wsl), Python3, python3-venv (Optional if you know what you're doing)

To run normally

$ source ./run.sh

To run using previously acquired user_games.json

$ source ./run.sh JSON

To run hiding sensitive info

$ source ./run.sh HIDE

To run using VSCode debug

$ source ./run.sh DEBUG

You can also look into the run.sh script to see how to run manually and can get help using the following:

$ python3 ./random_steam_game.py --help

INFO: If using this suggest running python3 -m pip install -r requirements.txt or setup your own virtual 
environment or whatever you want it's your life ;)