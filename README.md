💵 Finance App

Простое веб-приложение для учёта личных финансов, построенное по архитектуре MVC с использованием Flask, Bootstrap 5 и PostgreSQL.
🚀 Возможности

    💰 Учёт расходов и доходов

    🏷 Категории с вложенностью и типами (доход/расход)

    💳 Управление счетами (наличные, карта и т.д.)

    🔄 Переводы между счетами

    📊 Отчёты и аналитика:

        Сводка по категориям и периодам

        Графики и диаграммы

    📤 Экспорт в CSV / Excel

    🌙 Адаптивный интерфейс (Bootstrap 5)

🛠 Стек технологий

    Backend: Python 3 + Flask + SQLAlchemy

    Frontend: HTML + Bootstrap 5

    База данных: PostgreSQL

    Migrations: Alembic + Flask-Migrate

    Контейнеризация: Docker + Docker Compose (v2)

⚙️ Установка и запуск
📁 1. Клонируй репозиторий

git clone https://github.com/yourusername/finance-app.git
cd finance-app

🐳 2. Создай .env файл

POSTGRES_USER=finance_user
POSTGRES_PASSWORD=finance_pass
POSTGRES_DB=finance_db

▶️ 3. Запусти контейнеры

docker compose up --build --wait

После запуска приложение будет доступно по адресу:
http://localhost:5000
🗃 Структура проекта

app/
├── models/              # SQLAlchemy модели
├── controllers/         # Логика обработки данных
├── views/               # Flask маршруты (Blueprints)
├── templates/           # HTML-шаблоны (Jinja2)
├── static/              # Статические файлы (если нужно)
├── __init__.py          # Инициализация приложения
run.py                   # Точка входа Flask
docker-compose.yml       # Сборка и запуск

🧪 Миграции

flask db init          # Один раз
flask db migrate -m "initial"
flask db upgrade

📋 Планы на будущее

    Добавление мультивалютности

    Поддержка пользователей и авторизации

    Импорт выписок из банков

🧑‍💻 Автор

Разработано с ❤️ для личного использования.
Pull requests приветствуются!
