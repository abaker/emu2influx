FROM python:2.7

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python", "emu2influx.py"]

