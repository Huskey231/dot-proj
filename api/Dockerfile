FROM docker:latest

RUN apk add --no-cache --update python3

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["flask", "run"]