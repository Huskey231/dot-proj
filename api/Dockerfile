FROM docker:latest

WORKDIR /usr/src/api

RUN apk add --no-cache --update python3

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=api.app

ENTRYPOINT ["flask", "run"]
