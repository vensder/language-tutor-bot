FROM python:3.9.9-slim-buster

WORKDIR /usr/src/app/
COPY main.py requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

CMD PYTHONUNBUFFERED=1 python main.py
