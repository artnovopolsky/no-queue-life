FROM python:3.8

ENV TELEGRAM_API_TOKEN="token"

COPY nql_bot/requirements.txt /app/bot_requirements.txt
COPY nql_site/requirements.txt /app/site_requirements.txt

WORKDIR /app

RUN pip install -r /app/site_requirements.txt
RUN pip install -r /app/bot_requirements.txt

COPY . /app

CMD python /app/nql_bot/examples/run.py

