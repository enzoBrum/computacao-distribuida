from concurrent import futures
import logging
import os
import sys

from google.rpc import code_pb2, status_pb2
import grpc
from grpc import ServicerContext
from grpc_status import rpc_status
from psycopg2.errors import UniqueViolation

from config import connect_to_database
import polls_pb2
import polls_pb2_grpc
from users_pb2 import Empty, User
from users_pb2_grpc import UsersStub


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

PORT = os.getenv("PORT")


class PollServicer(polls_pb2_grpc.PollsServicer):

    def CreatePoll(self, request: polls_pb2.PollRequest, context: ServicerContext):

        logging.info("Criando enquete!")

        with connect_to_database() as cursor:
            insert_poll = """
            INSERT INTO polls (title, text, id_creator)
            values (%s, %s, %s) RETURNING id_poll;
            """
            cursor.execute(
                insert_poll, (request.poll.title, request.poll.text, request.user.id)
            )

            id_poll = cursor.fetchone()[0]

            cursor.executemany(
                "INSERT INTO option (text, id_poll) VALUES (%s, %s)",
                [(opt.text, id_poll) for opt in request.poll.options],
            )

        return Empty()

    def DeletePoll(self, request: polls_pb2.PollRequest, context: ServicerContext):
        logging.info("Deletando enquete...")

        with connect_to_database() as cursor:
            delete_poll = """
            DELETE FROM polls
            WHERE id = %s and creator_id = %s
            """
            cursor.execute(delete_poll, (request.id, request.user.id))

    def GetPolls(self, request: Empty, context: ServicerContext):
        logging.info("Listando todas as enquetes...")

        with connect_to_database() as cursor:
            select_polls = """
            SELECT id_poll, title, text
            FROM polls
            """

            cursor.execute(select_polls)
            poll_list = cursor.fetchall()

            select_options = """ 
            SELECT id_option, text
            FROM option
            WHERE id_poll = %s
            """

            options = {}

            ids = [poll[0] for poll in poll_list]
            for id in ids:
                cursor.execute(select_options, (id,))
                options[id] = cursor.fetchall()

            returned_polls = [
                polls_pb2.Poll(
                    id=poll[0],
                    title=poll[1],
                    text=poll[2],
                    options=[
                        polls_pb2.PollOptions(
                            id=options[poll[0]][i][0], text=options[poll[0]][i][1]
                        )
                        for i in range(len(options[poll[0]]))
                    ],
                )
                for poll in poll_list
            ]

        return polls_pb2.GetPollsReply(polls=returned_polls)

    def GetUserPolls(self, request: User, context: ServicerContext):
        logging.info("Listando todas as enquetes criadas pelo usuário...")

        with connect_to_database() as cursor:
            select_polls = """
            SELECT id_poll, title, text
            FROM polls
            where id_creator = %s
            """

            cursor.execute(select_polls, (request.id,))
            poll_list = cursor.fetchall()

            if poll_list == []:
                return polls_pb2.GetPollsReply(polls=[])

            select_options = """ 
            SELECT id_option, text
            FROM option
            WHERE id_poll = %s
            """

            options = {}

            ids = [poll[0] for poll in poll_list]
            for id in ids:
                cursor.execute(select_options, (id,))
                options[id] = cursor.fetchall()

            returned_polls = [
                polls_pb2.Poll(
                    id=poll[0],
                    title=poll[1],
                    text=poll[2],
                    options=[
                        polls_pb2.PollOptions(
                            id=options[poll[0]][i][0], text=options[poll[0]][i][1]
                        )
                        for i in range(len(options[poll[0]]))
                    ],
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

        try:
            with connect_to_database() as cursor:
                insert_vote = """
                INSERT INTO vote (id_user, id_option)
                VALUES (%s, %s)
                """
                cursor.execute(insert_vote, (request.id_user, request.id_option))
        except UniqueViolation:
            logging.info(
                "Usuário %s já votou em %s", request.id_user, request.id_option
            )

            context.abort_with_status(
                rpc_status.to_status(status_pb2.Status(code=code_pb2.ALREADY_EXISTS))
            )

        logging.info(f"{request.id_user} votou na opção {request.id_option}!")

        return Empty()

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

    def GetPollID(self, request: polls_pb2.Poll, context: ServicerContext):
        logging.info("Retornando ID da enquete...")

        with connect_to_database() as cursor:
            select_poll = """
            SELECT id_poll, title, text
            FROM polls
            WHERE id_poll = %s
            """
            cursor.execute(select_poll, (request.id,))
            poll = cursor.fetchone()
            logging.info(f"{poll=}")

            select_options = """ 
            SELECT o.id_option, o.text, COUNT(v.id_option) AS vote_count
            FROM (
                SELECT opt.id_option, opt.text FROM option opt WHERE opt.id_poll = %s
            ) o
            LEFT JOIN vote v ON
            v.id_option = o.id_option
            GROUP BY o.id_option, o.text
            ORDER BY o.text
            """

            cursor.execute(select_options, (poll[0],))
            options = cursor.fetchall()

            poll = polls_pb2.Poll(
                id=poll[0],
                title=poll[1],
                text=poll[2],
                options=[
                    polls_pb2.PollOptions(
                        id=options[i][0], text=options[i][1], votes=options[i][2]
                    )
                    for i in range(len(options))
                ],
            )

            return poll


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
