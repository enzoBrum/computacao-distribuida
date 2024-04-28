proto_install:
	pip install grpcio-tools
proto:
	python -m grpc_tools.protoc -I=./protos --python_out=./protos protos/*.proto --pyi_out=./protos --grpc_python_out=./protos
build: proto
	docker compose build --parallel
run: proto
	docker compose up
