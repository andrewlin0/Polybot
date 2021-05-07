FROM python:3.8.10-alpine3.13

ENV TZ=America/New_York \
    API_KEY=TWITTER_CONSUMER_KEY\
    API_SECRET_KEY=TWITTER_SECRET_CONSUMER_KEY \
    ACCESS_TOKEN=TWITTER_ACCESS_TOKEN \
    ACCESS_TOKEN_SECRET=TWITTER_SECRET_TOKEN \
    OPEN_WEATHER_KEY=OPEN_WEATHER_APIKEY \
    GOOGLE_PLACES_API_KEY=PLACES_API_KEY

COPY bots/config.py /bots/
COPY bots/polybot.py /bots/
COPY requirements.txt /tmp

RUN apk add gcc g++ musl-dev libffi-dev openssl-dev
RUN pip3 install -r /tmp/requirements.txt


WORKDIR /bots
CMD ["python3", "polybot.py"]