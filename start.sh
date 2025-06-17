#!/bin/bash
while true; do
    read -p "Удалить полностью данные контейнеров? [y/n]: " answer
    case "$answer" in
        [Yy])
            echo "Удаление подтверждено."
            docker compose down -v
            break
            ;;
        [Nn])
            echo "Запуск контейнеров без удаления данных."
            docker compose down
            break
            ;;
        *)
            echo "Пожалуйста, введите 'y' (yes) или 'n' (no)."
            ;;
    esac
done

docker compose up --build -d
docker compose exec web flask db upgrade

