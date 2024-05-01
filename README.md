# computacao-distribuida

## TODO

Esse é um TODO beeeeeeem inicial, só pra gente ter o esqueleto do trabalho. Depois que fizermos
tudo isso, vai ser fácil implementar identidade federada e front-end com HTML.
Veja o .proto para mais detalhes de cada rota.

OBS: à menos que você muda alguma das dependências em requirements.txt, não é necessário reiniciar os containers quando alguma mudança nos arquivos é realizada. Basta salvar o arquivo que
o serviço reinicia sozinho

### Compose

- [ ] achar uma forma de não ter que usar voluma pra montar o /protos

### Users

Por enquanto, não há necessidade de implementar identidade federada e hashing na senha do usuário.

- [ ] Criação/Deleção de usuário (Create e Delete)
  - Além do RPC, crie a rota `/signin` no front-end.
- [ ] Autenticação de usuário (Auth)
  - Crie a rota `/login` e a rota `/logout` no front-end e o RPC
- [ ] Obtenção de informações do usuário (GetInformation)
  - Por enquanto só o email

### Polls

OBS: Se as tabelas relacionadas à enquetes possuirem chaves estrangeiras pra tabela de usuários, vai ser necessário garantir que o serviço `users` inicia antes de `polls`

- [ ] Criação de uma enquete (CreatePoll)
  - Rota `/poll/create` no front-end e RPC
- [ ] Deleção de uma enquete (DeletePoll)
  - Rota `/poll/delete/<id>` no front-end e RPC
- [ ] Obtenção de todas as enquetes presentes na base de dados. (GetPolls)
  - Rota `/poll/all` no front-end e RPC
- [ ] Obtenção de todas as enquetes criadas por um usuário (GetUserPolls)
  - Rota `/poll/user/<id>` no front-end e RPC
- [ ] Votar em uma enquete (Vote)
  - Rota `/poll/vote/<id>` e RPC
- [ ] Remover o voto de uma enquete (Unvote)
  - Rota `/poll/unvote/<id>` e RPC

#### Testando o programa

Para testar a API, basta usar um comando semelhante à

```bash

# Pega todas as enquetes
curl localhost:80/poll/all

# Cria um usuário.
curl localhost:80/login -F name="Foo Bar" -F email=foo.bar@example.com -F password=1234
```

Eu implementei parte da criação de conta. Então da pra se basear naquilo quando for implementar a API e a comunicação com RPC.

## Tema:

- Sistema distribuído de votações

## Padrões de projeto utilizados:

- microserviços
- identidade federada
- replicação

## Tecnologias distribuidas

- A definir

## Funcionalidades

### Usuário Não Autenticado

- criar contas e se autenticar com serviços externos (Google)
- visualizar votações

### Usuário Autenticado

- criar, remover e alterar votações.
- votar em votações de outros usuários.
- alterar seus dados (caso não usa login com google)

## Linguagens, base de dados, etc

### Linguagens

- Interface: HTML puro
- Microserviços: python (flask)

### Base de dados:

- postgresql

### Identidade Federada

- Google

### Microserviços

- front-end: mostra o HTML.
- voting: criar, remover, alterar votos.
- users: criar, remover, alterar usuários. Além do login.

#### Rodando os microserviços

- ./run.sh
