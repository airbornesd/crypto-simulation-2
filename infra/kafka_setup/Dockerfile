FROM python:3.11-slim

WORKDIR /app

COPY infra/kafka_setup/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# these are now visible inside build context
COPY src ./src
COPY scripts ./scripts
COPY config ./config

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["python", "scripts/start_generator.py"]
