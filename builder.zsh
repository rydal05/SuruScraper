#!/bin/zsh
flask -app suruscrapr init-db
docker-compose up --build -d