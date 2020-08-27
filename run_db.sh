#!/usr/bin/env bash
docker stop swentech
docker rm swentech
docker run -d -p 5432 -e POSTGRES_PASSWORD=markup -e POSTGRES_USER=teodor -e POSTGRES_DB=teodor --name swentech postgres:10.5-alpine