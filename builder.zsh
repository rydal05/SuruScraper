#!/bin/zsh
flask -app server init-db
docker-compose up --build -d