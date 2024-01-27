FROM python:3

RUN python3 -m pip install -r requirements.txt

ENV TOKEN = "your_token"

COPY . /usr/bot

WORKDIR /usr/bot

CMD ["python3", "src/main.py"]
