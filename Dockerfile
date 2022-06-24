FROM python:3.10
WORKDIR ./
COPY ./bot ./bot
COPY ./.env ./bot
COPY ./app.py ./
COPY ./requirements.txt ./bot
RUN pip install -r ./bot/requirements.txt

WORKDIR ./

