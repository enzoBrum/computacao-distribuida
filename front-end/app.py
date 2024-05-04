import os

from flask import Flask, request
import grpc

from users_pb2 import Credentials, User, UserAuth
import users_pb2_grpc


app = Flask(__name__)

USERS_URL = os.environ["USERS_URL"]
POLLS_URL = os.environ["POLLS_URL"]


@app.route("/")
def hello_world():
    return "Olá, mundo!"


@app.route("/signin", methods=["POST"])
def sign_in():
    """
    Rota de criação de usuário.
    """

    # TODO: identidade federada
    # TODO: usar secure_channel

    params = request.form.to_dict(flat=True)

    name = params["name"]
    email = params["email"]
    password = params["password"]

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        user = User(name=name, email=email)
        cred = Credentials(password=password)

        stub.Create(UserAuth(user=user, credentials=cred))

    return "", 200

@app.route("/delete", methods=["POST"])
def delete():
    """
    Rota de para deleção de usuário.
    """

    params = request.form.to_dict(flat=True)

    email = params["email"]

    with grpc.insecure_channel(USERS_URL) as channel:
        stub = users_pb2_grpc.UsersStub(channel)

        user = User(email=email)

        stub.Delete(UserAuth(user=user))

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
    id_criador INT REFERENCES usuario(id_usuario)
)

create table opcao (
    id_opcao serial primary key,
    texto varchar(200) not null,
    quantidade int not null,
    id_enquete INT REFERENCES enquete(id_enquete)
)

create table voto (
    id_voto serial primary key,
    id_usuario int references usuario(id_usuario),
    id_enquete int references enquete(id_enquete)
)

"""
