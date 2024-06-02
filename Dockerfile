FROM alpine:latest

COPY . /discord

WORKDIR /discord

RUN apk add --no-cache --upgrade python3 py3-pip bash zip \
    && pip3 install --no-cache --break-system-packages -r requirements.txt \
    && find -type f -path "*.sh" | xargs chmod +x

VOLUME "/discord/logs/archives"

ENTRYPOINT "python3 -B main.py"