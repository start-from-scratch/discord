FROM python:3

RUN python3 -m pip3 install -r requirements.txt

COPY . /usr/bot

WORKDIR /usr/bot

CMD ["python3", "src/main.py"]