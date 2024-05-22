FROM alpine:latest

COPY . /discord

WORKDIR /discord

RUN apk add --no-cache --upgrade python3 py3-pip bash \
    && pip3 install --no-cache --break-system-packages -r requirements.txt

VOLUME "/discord/extensions/scripts" 

ENTRYPOINT "python3 -B main.py"
