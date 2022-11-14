FROM python:3.10-alpine

WORKDIR /home/app/MoneySaver

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add netcat-openbsd
RUN apk upgrade

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "/home/app/MoneySaver/entrypoint.sh"]
