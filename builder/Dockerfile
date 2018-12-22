FROM alpine:latest

WORKDIR /usr/src/build

RUN apk add --no-cache --update bash cmake make ruby python3 python2 g++ gcc nodejs openjdk8

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN pip3 install --no-cache-dir -e '.'

ENTRYPOINT ["dotproj_build"]
