import grp
import logging
import os
import sys

from flask import Flask, request, render_template, redirect, session
import grpc

from users_pb2 import AccessToken, Credentials, User, UserAuth, UsernamePassword
import users_pb2_grpc

from polls_pb2 import Poll, PollRequest, Vote

from google.rpc import code_pb2, status_pb2

# vscode vendo erro onde não tem.
from grpc_status import rpc_status # type: ignore

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

USERS_URL = os.environ["USERS_URL"]
POLLS_URL = os.environ["POLLS_URL"]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """
    Rota de criação de usuário.
    """

    # TODO: identidade federada
    # TODO: usar secure_channel

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return render_template("signup.html")

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        user = User(name=name, email=email)
        cred = Credentials(username_password=UsernamePassword(username=email, password=password))

        try:
            stub.Create(UserAuth(user=user, credentials=cred))
            return redirect("/index"), 200
        except grpc.RpcError as err:
            logger.error("Erro durante a criação da conta: %s", err)
            status: status_pb2.Status = rpc_status.from_call(err)

            if status.code == code_pb2.ALREADY_EXISTS:
                return f"Usuário com email {email} já existe!", 400
            return render_template("signup.html"), 500

@app.route("/delete", methods=["DELETE"])
def delete():
    """
    Rota de para deleção de usuário.
    """

    token = request.headers["Authorization"][6:]
    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        try:
            stub.Delete(Credentials(access_token=AccessToken(access_token=token)))
        except grpc.RpcError as err:
            logger.error("Erro durante a deleção do usuário", exc_info=True)
            status: status_pb2.Status = rpc_status.from_call(err)

            if status.code == code_pb2.UNAUTHENTICATED:
                return "", 401
            
            return "", 500

    return "", 200

@app.route("/login", methods=["GET", "POST"])
def log_in():
    name = request.form.get("name")
    password = request.form.get("password")

    if not name or not password:
        return render_template("login.html")

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        try:
            token: AccessToken = stub.GetToken(UsernamePassword(username=name, password=password))
            session["token"] = token.access_token
            return redirect("/index"), 200
        except grpc.RpcError as err:
            logger.error("Erro durante a obtenção do token", exc_info=True)
            status = rpc_status.from_call(err)

            if status.code == code_pb2.UNAUTHENTICATED:
                return render_template("login.html"), 401

            return render_template("login.html"), 500

@app.route("/poll/create", methods=["GET", "POST"])
def create_poll():
    """
    Rota de criação de enquete.
    """

    if "user_token" in session:
        token = session["user_token"]
    else:
        return redirect("/login")

    """with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        user = stub.Authenticate(Credentials(token=token))"""


    title = request.form.get("title")
    text = request.form.get("options")

    if not title or not text:
        return render_template("createpoll.html")

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        stub.CreatePoll(PollRequest(poll=Poll(title=title, text=text), user=user))

    return "", 200

@app.route("/poll/delete/<int:id>", methods=["POST"])
def delete_poll(id: int):
    """
    Rota de deleção de enquete.
    """

    token = request.headers["Authorization"][6:]

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        user = stub.Authenticate(Credentials(token=token))

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        stub.DeletePoll(PollRequest(poll=Poll(id=id), user=user))

    return "", 200


@app.route("/poll/user/<int:id>", methods=["GET"])
def get_user_polls(id: int):
    """
    Rota para obter enquetes de um usuário.
    """

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        polls = stub.GetUserPolls(User(id=id))

    return polls, 200

@app.route("/poll/vote/<int:id>", methods=["POST"])
def vote(id: int):
    """
    Rota para votar em uma enquete.
    """

    token = request.headers["Authorization"][6:]

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)
        user = stub.Authenticate(Credentials(token=token))

    with grpc.insecure_channel(POLLS_URL) as channel:
        stub = users_pb2_grpc.PollsStub(channel)
        stub.Vote(Vote(id_user=user.id, id_option=id))

    return "", 200



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
