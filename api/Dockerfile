# Базовый образ
FROM python:3.12-slim

# Чтобы Python нормально логировал и не плодил .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Системные зависимости (минимум)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код API
COPY . .

# Внутренний порт API
EXPOSE 9000

# Запуск FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "9000"]
