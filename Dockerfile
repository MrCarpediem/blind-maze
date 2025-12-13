FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN chmod +x scripts/run.sh

CMD ["sh", "scripts/run.sh"]
