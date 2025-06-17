💵 Finance App

Простое веб-приложение для учёта личных финансов, построенное по архитектуре MVC с использованием Flask, Bootstrap 5 и PostgreSQL.
  Возможности

    Учёт расходов и доходов

    Категории с вложенностью и типами (доход/расход)

    Управление счетами (наличные, карта и т.д.)

    Переводы между счетами

    Отчёты и аналитика:

        Сводка по категориям и периодам

    Адаптивный интерфейс (Bootstrap 5)


Установка и запуск

1. Клонируй репозиторий

git clone
cd finance-app

2. Создай .env файл

SECRET_KEY=secretkey
DATABASE_URL=postgresql://finance_user:finance_pass@db:5432/finance_db
FLASK_ENV=development
FLASK_APP=run.py


3. Запусти контейнеры

docker compose up --build --wait

После запуска приложение будет доступно по адресу:
http://localhost:5000

Миграции

flask db init          # Один раз

flask db migrate -m "initial"

flask db upgrade

  Планы на будущее

    Графики и диаграммы

    Экспорт в CSV / Excel

    Добавление мультивалютности

    Поддержка пользователей и авторизации

    Импорт выписок из банков

