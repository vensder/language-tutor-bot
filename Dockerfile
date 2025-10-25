# docker pull python:3.13.3-slim-bookworm
FROM python:3.13.3-slim-bookworm

WORKDIR /usr/src/app/
COPY main.py requirements.txt /usr/src/app/

RUN pip install  --no-cache-dir -r requirements.txt

CMD PYTHONUNBUFFERED=1 python main.py
