FROM python:3.13-slim AS builder

WORKDIR /usr/src/app

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./app/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Финальный образ ---
FROM python:3.13-slim

WORKDIR /usr/src/app

# Копируем "скомпилированные" wheel-зависимости из builder-стадии
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем код приложения
COPY ./app /usr/src/app/app

EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:5000", "--workers", "2", "app.app:create_app()"]

# Для запуска миграций локально (будет переопределено в Kubernetes Job)
# ENTRYPOINT ["python"]
# CMD ["app/migrate.py"]