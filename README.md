## run
```sh
echo 'TOKEN="your_token"' > .env
sudo apt-get update
sudo apt-get install git
git clone https://github.com/scratch-on-scratch/bot
cd bot

# run with docker
sudo apt-get install -y docker docker-compose
docker-compose up -d

# run without docker
sudo apt-get install -y python3 pip3
python3 -m pip3 install -r requirements.txt
python3 src/main.py 
```
