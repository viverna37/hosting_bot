FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# build deps для пакетов, которые могут компилиться
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# сначала зависимости — для кеша
COPY bot/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# потом код
COPY bot/ ./bot/
COPY config/ /app/config/

WORKDIR /app/bot
CMD ["python", "bot.py"]
