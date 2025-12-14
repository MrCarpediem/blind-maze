FROM python:3.10-slim

WORKDIR /app

RUN pip install pytest

COPY solution.sh run-tests.sh task.yaml dockercompose.yaml /app/
COPY tests /app/tests

RUN chmod +x /app/solution.sh /app/run-tests.sh

CMD ["./run-tests.sh"]
