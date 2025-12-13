FROM python:3.10-slim

WORKDIR /app

COPY maze ./maze
COPY scripts ./scripts

RUN chmod +x scripts/run.sh

CMD ["./scripts/run.sh"]
