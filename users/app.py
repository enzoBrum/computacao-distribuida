from concurrent import futures
import logging
import os
import sys

import grpc

from users_pb2 import Empty
import users_pb2_grpc

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

PORT = os.environ["PORT"]


class UserServicer(users_pb2_grpc.UsersServicer):
    """
    Prove métodos que implementam as funcionalidades do serviço de usuários
    """

    def Create(self, request, context) -> Empty:
        logging.debug(type(request))
        logging.debug(type(context))

        return Empty()


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UserServicer, server)

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    logging.debug("Servidor rodando na porta %s", PORT)
    server.wait_for_termination()
