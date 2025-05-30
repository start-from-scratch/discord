# Pixelbot

This repository contains the code of the dedicated bot of the discord server "[Start from Scratch](https://discord.gg/zQn3V5GSYK)".

## Requirements

You will need the [Go compiler](https://go.dev/) or the [Docker](https://www.docker.com/) depending on how you want to run it.

You will also need to create a `config.json` file following this schema:
```json
{
  "bot": {
    "token": "..."  //                 (required)
  },
  "metrics": {
    "delay": 10000, // in milliseconds (required)
    "port": "8080"  //                 (required)
  }
}
```

## Build & Run

Using [Go compiler](https://go.dev/)
```bash
go mod download
go build -o bot .
./bot
```

Using [Docker](https://www.docker.com/)
```bash
docker build -t bot .
docker run -d --name bot -p 8080:8080 --restart=unless-stopped bot
```