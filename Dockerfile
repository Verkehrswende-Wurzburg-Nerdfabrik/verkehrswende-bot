# Deriving the latest base image
FROM python:latest

WORKDIR /usr/app/src

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tweepy

COPY botConfig.py ./
COPY runBot.py ./

CMD [ "python", "./runBot.py"]
