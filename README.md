# computacao-distribuida

## TODO

OBS: à menos que você muda alguma das dependências em requirements.txt, não é necessário reiniciar os containers quando alguma mudança nos arquivos é realizada. Basta salvar o arquivo que
o serviço reinicia sozinho

### Padrões de projeto

- [ ] Identidade Federada.
- [ ] Replicação
- [x] Microserviços

### Tecnologias Distribuídas

- [x] RPC

### Front-end

- [ ] Mostrar enquetes na interface.
- [ ] Votar e desvotar a enquete. (Só quando ta logado.)
- [ ] Apagar enquete.
- [ ] Ver enqutes de usuário específico.

### Users

Por enquanto, não há necessidade de implementar identidade federada e hashing na senha do usuário.

- [x] Criação/Deleção de usuário (Create e Delete)
  - Além do RPC, crie a rota `/signin` no front-end.
- [x] Autenticação de usuário (Auth)
  - Crie a rota `/login` e a rota `/logout` no front-end e o RPC

### Polls

OBS: Se as tabelas relacionadas à enquetes possuirem chaves estrangeiras pra tabela de usuários, vai ser necessário garantir que o serviço `users` inicia antes de `polls`

- [x] Criação de uma enquete (CreatePoll)

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

## Tema:

- Sistema distribuído de votações

## Padrões de projeto utilizados:

- microserviços
- identidade federada
- replicação

## Tecnologias distribuidas

- RPC

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
