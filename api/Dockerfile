FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
  && pip install --no-cache-dir -r /app/requirements.txt

COPY api/ /app/api/
COPY config/ /app/config/
COPY database/ /app/database/

EXPOSE 9000
CMD ["python","-m","uvicorn","api.main:app","--host","0.0.0.0","--port","9000"]
