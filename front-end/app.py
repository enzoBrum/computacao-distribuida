from flask import Flask

import grpc

from users_pb2_grpc import UsersStub
from users_pb2 import User


app = Flask(__name__)



@app.route("/")
def hello_world():
    return "Olá, mundo!"


"""
Rotas:
    - / --> index.html. Página inicial
    - /vote/create --> cria voto
    - /vote/<id> --> vota em um voto.
    - /signin
    - /login
    - /logout
"""


if __name__ ==  "__main__":
    app.run(debug=True, host="0.0.0.0")


"""
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