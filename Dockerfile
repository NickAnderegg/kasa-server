FROM python:3 AS builder
COPY . /src
WORKDIR /src

ENV PYTHONPATH /src

RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
