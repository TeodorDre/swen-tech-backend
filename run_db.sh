#!/usr/bin/env bash
docker stop markup
docker rm markup
docker run -d -p 5432 -e POSTGRES_PASSWORD=markup -e POSTGRES_USER=markup -e POSTGRES_DB=markup --name markup postgres:10.5-alpine