# computacao-distribuida

## Executando a aplicação

Para executar a aplicação, rode o script `run.sh` na pasta raíz do projeto.
É necessário que o docker esteja instalado e que a porta 5000 esteja livre.

Quando a aplicação já estiver executando, basta acessar `localhost:5000/` no navegador.

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
