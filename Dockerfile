FROM python:3.12.4

COPY . /discord

WORKDIR /discord

RUN python3 -m pip install --no-cache -r requirements.txt

VOLUME "/discord/logs/archives"

ENTRYPOINT "python3 -B main.py"