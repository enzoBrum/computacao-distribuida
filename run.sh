#!/bin/sh

python -m grpc_tools.protoc -I=./protos --python_out=./protos protos/*.proto --pyi_out=./protos --grpc_python_out=./protos
docker compose build --parallel
docker compose up
