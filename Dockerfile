FROM python:3.8

ENV TELEGRAM_API_TOKEN="${TELEGRAM_API_TOKEN}"

COPY nql_bot/requirements.txt /app/bot_requirements.txt

WORKDIR /app

RUN pip install -r /app/bot_requirements.txt

COPY . /app
RUN pip install /app/nql_bot/

CMD python /app/nql_bot/examples/run.py

