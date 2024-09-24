FROM python:3.12-slim as builder 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --target=/install -r requirements.txt

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/install

COPY --from=builder /install /install
COPY . /app

WORKDIR /app

RUN useradd --no-log-init -M appuser && \
    chown -R appuser /app && \ 
    chmod +x /app/start.sh 

ENV PATH="/install/bin:$PATH"

USER appuser

EXPOSE 8080

CMD ["sh", "/app/start.sh"]