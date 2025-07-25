FROM python:3.12-slim

WORKDIR /app

# Копируем только requirements.txt для кэширования слоя зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код, игнорируя файлы из .dockerignore
COPY . .

# Запускаем только приложение, миграции лучше запускать отдельно
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"]