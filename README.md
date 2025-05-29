# Pixelbot

This repository contains the code of the dedicated bot of the discord server "[Start from Scratch](https://discord.gg/zQn3V5GSYK)".

## Usage

Using [Go compiler](https://go.dev/)
```bash
go mod download
go build -o bot .
./bot
```

Using [Docker](https://www.docker.com/)
```bash
docker build -t bot .
docker run -d --restart=unless-stopped --name bot bot
```