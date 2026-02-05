FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY bot/ ./bot/
RUN pip install --no-cache-dir -r requirements.txt

# если bot.py лежит прямо в bot/ и запускается так:
WORKDIR /app/bot
CMD ["python", "bot.py"]
