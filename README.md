# Node_task

## Описание

Проект на FastAPI с использованием Alembic для миграций и Docker для контейнеризации. Используется PostgreSQL как база данных.

---

## Быстрый старт

### 1. Клонируйте репозиторий
```bash
# git clone https://github.com/CapitanGrant/node_task
# cd Node_task
```

### 2. Настройте переменные окружения

```
DB_USER=postgres_user
DB_PASSWORD=postgres_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=postgres_db
```

### 3. Соберите и запустите контейнеры
```bash
docker-compose up --build
```
### 4. Перейдите по ссылке для тестирования приложения

```
http://127.0.0.1:8001/docs#/
```


## Основные команды

- Запуск приложения:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
  ```


## Структура проекта
- `app/` — исходный код приложения
- `app/tasks/` — бизнес-логика задач
- `app/dao/` — работа с БД
- `app/migration/` — миграции Alembic

---

## Зависимости
Указаны в `requirements.txt`. Основные:
- fastapi
- uvicorn
- alembic
- loguru

---
