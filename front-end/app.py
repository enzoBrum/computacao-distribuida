import base64
from functools import wraps
import grp
import json
import logging
import os
import sys

from flask import Flask, redirect, render_template, request, session
from flask import g
from google.rpc import code_pb2, status_pb2
import grpc
from grpc_status import rpc_status

from polls_pb2 import GetPollsReply, Poll, PollOptions, PollRequest, VoteInfo
import polls_pb2_grpc
from users_pb2 import AccessToken, Credentials, Empty, User, UserAuth, UsernamePassword
import users_pb2_grpc

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = "a4555ba2625e9496efc5ee371181ed9d5831165c28199bed1d758499cde4f2e6"


USERS_URL = os.environ["USERS_URL"]
POLLS_URL = os.environ["POLLS_URL"]


def get_info_from_token(token: str, info: str, default: any = None) -> str:
    token = token.split(".")[1]
    token_padded = (
        token if len(token) % 4 == 0 else token + "=" * (4 - (len(token) % 4))
    )

    token_json: dict[str, any] = json.loads(base64.b64decode(token_padded).decode())
    return token_json.get(info, default)


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = session.get("token") or request.headers.get("Authorization", "")[7:]
        if not token:
            redirect("/login")

        with grpc.insecure_channel(USERS_URL) as channel:
            stub = users_pb2_grpc.UsersStub(channel)

            try:
                user = stub.Auth(Credentials(access_token=AccessToken(token=token)))

                g.user = user
            except grpc.RpcError as err:
                logger.error("Erro durante autenticação", exc_info=True)
                status: status_pb2.Status = rpc_status.from_call(err)

                if status.code == code_pb2.NOT_FOUND:
                    return render_template(
                        "index.html", error=True, error_msg="User not found"
                    )
                elif status.code == code_pb2.UNAUTHENTICATED:
                    return render_template(
                        "index.html", error=True, error_msg="User credentials are wrong"
                    )
                return render_template(
                    "index.html", error=True, error_msg="Unknown error."
                )
            except Exception as err:
                logger.error("Erro durante autenticação", exc_info=True)
                return render_template(
                    "index.html", error=True, error_msg="Unknown error."
                )
            else:
                return func(*args, **kwargs)

    return wrapper


@app.route("/")
@app.route("/index")
def index():
    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = polls_pb2_grpc.PollsStub(channel)

        polls: GetPollsReply = stub.GetPolls(Empty())

    if session.get("token") is not None:
        token = session["token"]
        logger.debug(token)
        username = get_info_from_token(token, "sub")
        return render_template("index.html", username=username, polls=polls.polls)
    else:
        return render_template("index.html", polls=polls.polls)


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """
    Rota de criação de usuário.
    """

    # TODO: identidade federada

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return render_template("signup.html")

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        user = User(name=name, email=email)
        cred = Credentials(
            username_password=UsernamePassword(username=email, password=password)
        )

        try:
            stub.Create(UserAuth(user=user, credentials=cred))
            access_token: AccessToken = stub.GetToken(
                UsernamePassword(username=email, password=password)
            )
            session["token"] = access_token.token
            logger.debug(session["token"])
            return redirect("/index")
        except grpc.RpcError as err:
            logger.error("Erro durante a criação da conta: %s", err)
            status: status_pb2.Status = rpc_status.from_call(err)

            if status.code == code_pb2.ALREADY_EXISTS:
                return render_template(
                    "signup.html",
                    error=True,
                    error_msg=f"Usuário com email {email} já existe!",
                )
            return render_template("signup.html", error=True, error_msg="unknown error")


@app.route("/logout")
def logout():
    if session.get("token") is not None:
        session.clear()
    return redirect("/index")


@app.route("/delete", methods=["DELETE"])
@authenticate
def delete():
    """
    Rota de para deleção de usuário.
    """

    token = request.headers["Authorization"][6:]
    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        try:
            stub.Delete(Credentials(access_token=AccessToken(token=token)))
        except grpc.RpcError as err:
            logger.error("Erro durante a deleção do usuário", exc_info=True)
            status: status_pb2.Status = rpc_status.from_call(err)

            if status.code == code_pb2.UNAUTHENTICATED:
                return "", 401

            return "", 500

    return "", 200


@app.route("/login", methods=["GET", "POST"])
def log_in():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        logger.info("Sem email ou senha")
        return render_template(
            "login.html",
        )

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        try:
            access_token: AccessToken = stub.GetToken(
                UsernamePassword(username=email, password=password)
            )
            session["token"] = access_token.token
            logger.info("Login bem-sucedido")
            return redirect("/index")
        except grpc.RpcError as err:
            logger.error("Erro durante a obtenção do token", exc_info=True)
            status = rpc_status.from_call(err)

            if status.code == code_pb2.UNAUTHENTICATED:
                return (
                    render_template(
                        "login.html",
                        error=True,
                        error_msg="invalid email or password",
                    ),
                    401,
                )

            return (
                render_template("login.html", error=True, error_msg="unknown error"),
                500,
            )


@app.route("/token", methods=["POST"])
def get_token():
    email, password = request.form.get("email"), request.form.get("password")

    if email is None or password is None:
        return "Email or Password not provided", 400

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        try:
            access_token: AccessToken = stub.GetToken(
                UsernamePassword(username=email, password=password)
            )
            return access_token.token, 200
        except grpc.RpcError as err:
            logger.error("Erro durante a obtenção do token", exc_info=True)
            status = rpc_status.from_call(err)

            if status.code == code_pb2.UNAUTHENTICATED:
                return "invalid email or password", 401

            return "", 500


@app.route("/poll/create", methods=["GET", "POST"])
@authenticate
def create_poll():
    """
    Rota de criação de enquete.
    """

    token = session["token"]
    logger.debug(token)
    username = get_info_from_token(token, "sub")

    title = request.form.get("title")
    text = request.form.get("content")
    options = request.form.get("options")

    if not title or not text or not options:
        return render_template("createpoll.html", username=username)

    options = options.split(";")

    logger.info(f"Criando enquete. {title=}, {text=}, {options=}")
    logger.info(f"g.user: {g.user}")

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = polls_pb2_grpc.PollsStub(channel)

        poll = Poll(
            title=title, text=text, options=[PollOptions(text=opt) for opt in options]
        )

        stub.CreatePoll(PollRequest(poll=poll, user=g.user))

    return redirect("/index")


@app.route("/poll/delete/<int:id>", methods=["POST"])
@authenticate
def delete_poll(id: int):
    """
    Rota de deleção de enquete.
    """

    token = request.headers["Authorization"][6:]

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        stub.DeletePoll(PollRequest(poll=Poll(id=id), user=g.user))

    return "", 200


@app.route("/poll/user/<int:id>", methods=["GET"])
@authenticate
def get_user_polls(id: int):
    """
    Rota para obter enquetes de um usuário.
    """

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        polls = stub.GetUserPolls(User(id=id))

    return polls, 200


@app.route("/poll/vote/<int:id>", methods=["GET", "POST"])
@authenticate
def vote(id: int):
    """
    Rota para votar em uma enquete.
    """

    token = session["token"]
    logger.debug(token)
    username = get_info_from_token(token, "sub")

    id_options_marked = []

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = polls_pb2_grpc.PollsStub(channel)

        poll: Poll = stub.GetPollID(Poll(id=id))

        for option in poll.options:
            if request.form.get(str(option.id)) is not None:
                id_options_marked.append(option.id)

        if len(id_options_marked) == 0:
            return render_template("vote.html", username=username, poll=poll)

        already_voted = set()
        for id_option in id_options_marked:
            try:
                stub.Vote(VoteInfo(id_user=g.user.id, id_option=id_option))
            except grpc.RpcError as err:
                logger.error("Erro durante o voto %s", id_option, exc_info=True)

                status: status_pb2.Status = rpc_status.from_call(err)

                if status.code == code_pb2.ALREADY_EXISTS:
                    already_voted.add(id_option)
                else:
                    raise err

        if len(already_voted) > 0:
            option_texts = [opt.text for opt in poll.options if opt.id in already_voted]
            return render_template(
                "vote.html",
                username=username,
                poll=poll,
                error=True,
                error_msg=f"Já votou nas seguintes opções: {','.join(option_texts)}",
            )
    return redirect("/index")


if __name__ == "__main__":
    app.run(host="0.0.0.0")


"""


Rotas:
    - / --> index.html. Página inicial
    - /vote/create --> cria voto
    - /vote/<id> --> vota em um voto.
    - /signin
    - /login
    - /logout

create table usuario (
    id_usuario serial primary key,
    nome varchar(50) not null,
    email varchar(50) not null,
    senha varchar(50)
);

create table enquete (
    id_enquete serial primary key,
    texto varchar(200) not null,
    titulo varchar(50) not null,
    id_criador INT 
)

create table opcao (
    id_opcao serial primary key,
    texto varchar(200) not null,
    quantidade int not null,
    id_enquete INT REFERENCES enquete(id_enquete)
)

create table voto (
    id_voto serial primary key,
    id_usuario int
    id_enquete int references opcao(id_opcao)
)

"""
