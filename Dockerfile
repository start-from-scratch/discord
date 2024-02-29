FROM python:3.8.9

COPY . /usr/containers/pixelbot

WORKDIR /usr/containers/pixelbot

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "-B", "src/main.py" ]