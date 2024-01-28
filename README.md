## Run
To run the bot you need to execute the bash code wrote below.
```sh
apt-get update
apt-get install git python3 pip

git clone https://github.com/scratch-on-scratch/bot 
cd bot

python3 -m venv venv
python3 -m pip install -r requirements.txt
python3 src/main.py
```
Warning: Make sure to have defined a valid token in `config.json` before running the bot.
-
