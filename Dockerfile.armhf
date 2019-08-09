FROM alpine:latest

RUN \
 apk add curl && \
 curl -L https://github.com/balena-io/qemu/releases/download/v3.0.0%2Bresin/qemu-3.0.0+resin-arm.tar.gz | tar --strip=1 -zxvf -

FROM arm32v7/python:2.7.16-buster

COPY --from=0 /qemu-arm-static /usr/bin

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python", "emu2influx.py"]

