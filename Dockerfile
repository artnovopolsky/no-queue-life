FROM python:3.8

COPY nql_bot/requirements.txt nql_site/requirements.txt 

WORKDIR /nql  

RUN pip install -r /nql_bot/requirements.txt

COPY . /nql

CMD python /nql/nql_bot/examples/run.py

