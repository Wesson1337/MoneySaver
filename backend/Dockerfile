FROM python:3.10-alpine3.16

WORKDIR /home/app/MoneySaver

RUN mkdir backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk upgrade
RUN apk add netcat-openbsd && apk add postgresql-dev gcc python3-dev musl-dev

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ./backend

ENTRYPOINT ["sh", "/home/app/MoneySaver/backend/entrypoint.sh"]
