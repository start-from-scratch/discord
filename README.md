# Pixelbot
## Fonctionnement
Vous devez tout d'abord préparer le robot.
```bash
apt-get update
apt-get install -y git

git clone https://github.com/start-from-scratch/pixelbot

cd pixelbot
```

Vous devez avant de le mettre en route remplir les informations manquantes dans `config.json` en utilisant par exemple :
```bash
echo '{ "status_channel_id": [ <ids> ] , "token": <token> }' > config.json
```

Pour faire fonctionner le robot sur une courte durée :
```bash
apt-get install -y python3 python3-pip python3-venv

python3 -m venv venv
python3 -m pip install -r requirements.txt
python3 src/main.py
```

Pour faire fonctionner le robot sur une longue durée:
```bash
apt-get install -y podman

podman build -t pixelbot .
podman run --name pixelbot -d pixelbot
```
