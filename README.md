## Fonctionnement
Vous devez tout d'abord préparer le robot.
```bash
apt-get update
apt-get install -y git

git clone https://github.com/start-from-scratch/pixelbot

cd pixelbot
echo "votre_token" > token.txt
```

Pour faire fonctionner le robot sur une courte durée :
```bash
apt-get install -y python3 python3-pip

pip install -r requirements.txt
python3 src/main.py
```

Pour faire fonctionner le robot sur une longue durée:
```bash
apt-get install -y podman

podman build -t pixelbot .
podman run --name pixelbot -d pixelbot
```