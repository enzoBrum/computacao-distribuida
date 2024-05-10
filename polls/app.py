from concurrent import futures
import logging
import os
import sys

import grpc
from grpc import ServicerContext

from config import connect_to_database
import polls_pb2
import polls_pb2_grpc
from users_pb2 import User
from users_pb2_grpc import UsersStub

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

PORT = os.getenv("PORT")


class PollServicer(polls_pb2_grpc.PollsServicer):

    def CreatePoll(self, request: polls_pb2.PollRequest, context: ServicerContext):

        logging.info("Criando enquete!")

        with connect_to_database() as cursor:
            insert_poll = """
            INSERT INTO polls (tittle, text, creator_id)
            values (%s, %s, %s)
            """
            cursor.execute(
                insert_poll, (request.poll.title, request.poll.text, request.user.id)
            )

    def DeletePoll(self, request: polls_pb2.PollRequest, context: ServicerContext):
        logging.info("Deletando enquete...")

        with connect_to_database() as cursor:
            delete_poll = """
            DELETE FROM polls
            WHERE id = %s and creator_id = %s
            """
            cursor.execute(delete_poll, (request.id, request.user.id))

    def GetPolls(self, request: polls_pb2.PollRequest, context: ServicerContext):
        logging.info("Listando todas as enquetes...")

        with connect_to_database() as cursor:
            query = "SELECT * FROM polls"
            cursor.execute(query)
            poll_list = cursor.fetchall()
            for i in poll_list:
                logging.info(i)  # ?

    def GetUserPolls(self, request: User, context: ServicerContext):
        logging.info("Listando todas as enquetes criadas pelo usuário...")

        with connect_to_database() as cursor:
            select_polls = """
            SELECT id_poll, text, tittle
            FROM polls 
            WHERE polls.id_creator = %s"""

            result = cursor.execute(select_polls, (request.id,))
            poll_list = result.fetchall()

            select_options = """ 
            SELECT id_option, text
            FROM options
            WHERE id_poll = %s
            """

            options = {}

            ids = [poll[0] for poll in poll_list]
            for id in ids:
                result = cursor.execute(select_options, (id,))
                options[id] = result.fetchall()

            returned_polls = [
                polls_pb2.Poll(
                    poll[0], poll[1], poll[2], polls_pb2.PollOptions(options[poll[0]])
                )
                for poll in poll_list
            ]

        return polls_pb2.GetPollsReply(polls=returned_polls)

    def GetPollsVotedByUser(self, request, context):
        with connect_to_database() as cursor:
            query = """SELECT p.* FROM polls p
                    JOIN options o ON o.id_poll = p.id_poll
                    JOIN votes v ON v.id_option = o.id_option
                    WHERE v.id_user = %s"""
            cursor.execute(query, (request.user.id))
            poll_list = cursor.fetchall()
            for i in poll_list:
                logging.info(i)  # ?

    def Vote(self, request: polls_pb2.VoteInfo, context: ServicerContext):
        logging.info("Votando...")

        with connect_to_database() as cursor:
            insert_vote = """
            INSERT INTO vote (id_user, id_option)
            VALUES (%s, %s)
            """
            cursor.execute(insert_vote, (request.id_user, request.id_option))

        logging.info(f"{request.user.name} votou na opção {request.option}!")

    def Unvote(self, request: polls_pb2.VoteInfo, context: ServicerContext):
        logging.info("Removendo o voto...")

        with connect_to_database() as cursor:
            delete_vote = """
            DELETE FROM vote 
            WHERE id_user = %s AND id_option = %s
            """
            cursor.execute(delete_vote, (request.id_user, request.id_option))

        logging.info(
            f"Removido o voto de {request.user.name} na opção {request.option}!"
        )


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    polls_pb2_grpc.add_PollsServicer_to_server(PollServicer(), server)

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    logging.info("Servidor rodando na porta %s", PORT)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Execuçao encerrada")
        exit(0)


if __name__ == "__main__":
    main()

