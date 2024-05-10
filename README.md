# Pixelbot
## Fonctionnement
```bash
apt-get update
apt-get install -y git

git clone https://github.com/start-from-scratch/pixelbot .
```

Il est possible que vous deviez ajouter des valeurs dans `config.json`.

```bash
apt-get install -y python3 python3-pip python3-venv

python3 -m venv venv
python3 -m pip install -r requirements.txt
python3 main.py
```

```bash
apt-get install -y docker-ce

docker build -t pixelbot .
docker run -d --name pixelbot --restart unless-stopped pixelbot
```
