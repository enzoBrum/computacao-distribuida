from concurrent import futures
import logging
import os
import sys

import grpc
from sqlalchemy.orm import Session

from config import DbUser, engine, init_db
import users_pb2
import users_pb2_grpc

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

PORT = os.getenv("PORT")


class UserServicer(users_pb2_grpc.UsersServicer):
    """
    Prove métodos que implementam as funcionalidades do serviço de usuários
    """

    def Create(self, request: users_pb2.UserAuth, context) -> users_pb2.Empty:

        # TODO: lidar com emails repetidos.

        logging.info("Adicionando usuário %s na base de dados...", request.user.name)

        user = DbUser(
            id=None,
            name=request.user.name,
            email=request.user.email,
            password=request.credentials.password,
        )

        with Session(engine()) as session:
            existing_user = session.query(DbUser).filter(DbUser.email == request.user.email).first()
            if existing_user:
                logging.info("Email já cadastrado.")
                return users_pb2.Empty()
            
            session.add(user)
            session.commit()

        return users_pb2.Empty()

    def Delete(self, request: users_pb2.UserAuth, context) -> users_pb2.Empty:

        logging.info("Removendo usuário da base de dados...")

        with Session(engine()) as session:
            user = session.query(DbUser).filter(DbUser.email == request.user.email).first()
            if not user:
                logging.info("Usuário não encontrado.")
                return users_pb2.Empty()
            
            session.delete(user)
            session.commit()

            logging.info(f"Usuário {user} removido com sucesso.")

        return users_pb2.Empty()

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(UserServicer(), server)

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    logging.info("Servidor rodando na porta %s", PORT)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Execuçao encerrada")
        exit(0)


if __name__ == "__main__":
    init_db()
    main()
