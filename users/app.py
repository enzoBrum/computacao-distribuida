from concurrent import futures
import logging
import os
import sys

import grpc

from config2 import connect_to_database, init_db 
from authlib import jose
import users_pb2
import users_pb2_grpc
    
from psycopg2.errors import UniqueViolation

from google.rpc import code_pb2, status_pb2
from google.protobuf import any_pb2

from grpc import ServicerContext

# vscode ta vendo erro onde não tem
from grpc_status import rpc_status # type: ignore
from time import time

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

PORT = os.getenv("PORT")
with open("public-key.pem") as pub, open("private-key.pem") as priv:
    PUBLIC_KEY = pub.read()
    PRIVATE_KEY = priv.read()

TOKEN_EXPIRATION_TIME_SECONDS = os.getenv("TOKEN_EXPIRATION", 3600)


class UserServicer(users_pb2_grpc.UsersServicer):
    """
    Prove métodos que implementam as funcionalidades do serviço de usuários
    """
    
    def __create_jwt(self, username: str) -> str:
        header = {"alg": "RS256"}
        payload = {
            "sub": username,
            "iat": time(),
            "exp": time() + TOKEN_EXPIRATION_TIME_SECONDS,
            "iss": "users-service",
        }

        return jose.jwt.encode(header, payload, PRIVATE_KEY)
    

    def __authenticate(self, credentials: users_pb2.Credentials, context: ServicerContext) ->  None:
        
        result = True
        if credentials.access_token is not None:
            try:
                token = jose.jwt.decode(credentials.access_token.access_token, PUBLIC_KEY)
                result = time() < token["exp"]
            except Exception:
                logging.error("Assinatura inválida")

        if credentials.username_password is not None:
            with connect_to_database() as cursor:
                username = credentials.username_password.username
                password = credentials.username_password.password
                cursor.execute(
                    "SELECT id_user FROM users WHERE email=%s AND password=%s",
                    (username, password)
                )

                result = cursor.fetchone() is not None

        if not result:
            context.abort_with_status(rpc_status.to_status(status_pb2.Status(code=code_pb2.UNAUTHENTICATED)))


    def Create(self, request: users_pb2.UserAuth, context: ServicerContext) -> users_pb2.Empty:
        logging.info("Adicionando usuário %s na base de dados...", request.user.name)


        try:
            with connect_to_database() as cursor:
                insert_user = """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_user, (request.user.name, request.user.email, request.credentials.username_password.password))
                logging.info("Usuário %s adicionado com sucesso", request.user.name)
        except UniqueViolation:
            logging.info("Usuário com email %s já existe...", request.user.email)
            context.abort_with_status(
                rpc_status.to_status(
                    status_pb2.Status(code=code_pb2.ALREADY_EXISTS, message=f"User with email {request.user.email} already exists")
                )
            )

        return users_pb2.Empty()

    def Delete(self, request: users_pb2.Credentials, context: ServicerContext) -> users_pb2.Empty:
        logging.info("Removendo usuário da base de dados...")

        self.__authenticate(request, context)

        # email = 
        with connect_to_database() as cursor:
            delete_user = """
            DELETE FROM users
            WHERE email = %s;
            """

            cursor.execute(delete_user, (request.access_token.access_token,))

        return users_pb2.Empty()
    
    def Auth(self, request: users_pb2.Credentials, context: ServicerContext) -> users_pb2.AuthReply:
        self.__authenticate(request, context)

        if request.username_password is not None:
            email = request.username_password.username
        else:
            email = jose.jwt.decode(request.access_token.access_token)
        with connect_to_database() as cursor:
            cursor.execute("SELECT id_user, name, email FROM users WHERE email=%s", (email,))
            usr = cursor.fetchone()
            if usr is None:
                context.abort_with_status(rpc_status.to_status(status_pb2.Status(code=code_pb2.NOT_FOUND)))
            id, name, email = cursor.fetchone()[0]
            return users_pb2.User(name=name, email=email, id=id)
        

    def GetToken(self, request: users_pb2.UsernamePassword, context: ServicerContext) -> users_pb2.AccessToken:
        self.__authenticate(users_pb2.Credentials(username_password=request), context)

        return users_pb2.AccessToken(access_token=self.__create_jwt(request.username))

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
