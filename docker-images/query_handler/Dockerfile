FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV IS_RUNNING_IN_DOCKER=True

EXPOSE 8765

CMD ["python3", "server.py"]