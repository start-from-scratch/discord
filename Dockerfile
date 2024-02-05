FROM python:3.8.9

ENV TOKEN "MTEyNjQyOTkyODYxMTY0MzU0NA.G5eC3W.gySwdBcRIi0GoHyMQGFNSHWL6U7ep64G6AatG4"

COPY . /usr/containers/pixelbot

WORKDIR /usr/containers/pixelbot

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "src/main.py" ]