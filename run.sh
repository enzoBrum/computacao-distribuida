#!/bin/sh

docker rm -f $(docker ps -qa)

docker compose build --parallel
docker compose up
