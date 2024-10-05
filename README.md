# Pixelbot


## Usage

```sh
git clone https://github.com/swtchcoder/python-discord
cd python-discord
```

<details open>
<summary>Base</summary>

```sh
python3 -m pip install -r requirements.txt
python3 main.py
```
</details>

<details>
<summary>Docker</summary>
    
```sh
docker build -t pixelbot .
docker run -d --name pixelbot --restart unless-stopped pixelbot
```
</details>
