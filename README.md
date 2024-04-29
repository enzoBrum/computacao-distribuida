# computacao-distribuida

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
