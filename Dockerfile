FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    WORKSPACE_ROOT=/app/workspace

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/workspace/projects /app/workspace/datasets /app/workspace/exports /app/workspace/.history

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "gthread", "--threads", "8", "-w", "1", "backend.app:app", "--bind", "0.0.0.0:5000", "--timeout", "180"]
