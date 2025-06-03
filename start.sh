#!/bin/bash
docker compose down -v
docker stop $(docker ps -q);docker system prune -a --volumes
docker compose up --build -d
docker compose exec web flask db migrate -m "initial"
docker compose exec web flask db upgrade

