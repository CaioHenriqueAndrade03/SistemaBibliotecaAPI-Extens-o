# Sistema de Biblioteca

API REST para controle de livros, sócios e empréstimos, desenvolvida com **FastAPI + PostgreSQL** e executada em containers Docker.

---

## Tecnologias utilizadas

| Camada       | Tecnologia                  |
|--------------|-----------------------------|
| Linguagem    | Python 3.12                 |
| Framework    | FastAPI 0.111               |
| ORM          | SQLAlchemy 2.0              |
| Banco        | PostgreSQL 16               |
| Containers   | Docker + Docker Compose     |
| Editor       | VSCode                      |

---

## Arquitetura do projeto
<img width="565" height="410" alt="image" src="https://github.com/user-attachments/assets/65155e73-3f4e-4783-92dc-e8f0a8e55435" />

---

## Estrutura do projeto

```
biblioteca/
├── app/
│   ├── db/           # Conexão com o banco (SQLAlchemy)
│   ├── models/       # Modelos das tabelas
│   ├── routers/      # Rotas da API (livros, socios, emprestimos, resumo)
│   ├── schemas/      # Schemas Pydantic (validação de entrada/saída)
│   ├── config.py     # Variáveis de ambiente
│   └── main.py       # Ponto de entrada da aplicação
├── sql/
│   └── init.sql      # Script de criação das tabelas
├── Dockerfile              # Imagem de desenvolvimento
├── Dockerfile.prod         # Imagem de produção (multi-stage)
├── docker-compose.yml      # Ambiente de desenvolvimento
├── docker-compose.prod.yml # Ambiente de produção
├── requirements.txt
└── .env.example
```

---

## Como executar em desenvolvimento

```bash
# 1. Clone o projeto e entre na pasta
cd biblioteca

# 2. Suba os containers
docker compose up --build

# 3. Acesse a documentação interativa
# http://localhost:8000/docs
```

O código é montado como volume — qualquer alteração no código recarrega o servidor automaticamente.

---

## Como executar em produção

```bash
# 1. Crie o arquivo .env a partir do exemplo
cp .env.example .env

# 2. Edite o .env com senhas seguras
# DB_PASSWORD=troque_esta_senha

# 3. Suba com o compose de produção
docker compose -f docker-compose.prod.yml up --build -d
```

---

## Portas utilizadas

| Serviço     | Porta (dev) | Porta (prod) |
|-------------|-------------|--------------|
| API         | 8000        | 8000         |
| FrontEn     | 5500        | 5500         |
| PostgreSQL  | 5432        | não exposta  |

---

## Endpoints principais

### Livros
| Método | Rota                  | Descrição                        |
|--------|-----------------------|----------------------------------|
| POST   | `/livros/`            | Cadastra um livro                |
| GET    | `/livros/`            | Lista todos os livros            |
| GET    | `/livros/disponiveis` | Lista livros com estoque > 0     |
| GET    | `/livros/{id}`        | Busca livro por ID               |

### Sócios
| Método | Rota           | Descrição              |
|--------|----------------|------------------------|
| POST   | `/socios/`     | Cadastra um sócio      |
| GET    | `/socios/`     | Lista todos os sócios  |
| GET    | `/socios/{id}` | Busca sócio por ID     |

### Empréstimos
| Método | Rota                              | Descrição                   |
|--------|-----------------------------------|-----------------------------|
| POST   | `/emprestimos/`                   | Efetua um empréstimo        |
| PATCH  | `/emprestimos/{id}/devolver`      | Registra devolução          |
| GET    | `/emprestimos/`                   | Lista todos os empréstimos  |
| GET    | `/emprestimos/abertos`            | Lista empréstimos em aberto |

### Resumo
| Método | Rota       | Descrição                            |
|--------|------------|--------------------------------------|
| GET    | `/resumo/` | Total de livros, sócios e em aberto  |

---

## Exemplos de uso

### Cadastrar um livro
```json
POST /livros/
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano_publicacao": 1899,
  "isbn": "978-85-359-0277-5",
  "quantidade_total": 3
}
```

### Cadastrar um sócio
```json
POST /socios/
{
  "nome": "Ana Souza",
  "email": "ana@email.com",
  "telefone": "11999990000"
}
```

### Efetuar um empréstimo
```json
POST /emprestimos/
{
  "livro_id": 1,
  "socio_id": 1,
  "data_prevista_devolucao": "2026-06-10"
}
```

### Devolver um livro
```
PATCH /emprestimos/1/devolver
(sem corpo — apenas o ID na URL)
```

---

## Regras de negócio

- Um livro só pode ser emprestado se houver ao menos 1 exemplar disponível.
- Ao efetuar empréstimo, `quantidade_disponivel` é decrementada.
- Ao devolver, `quantidade_disponivel` é incrementada.
- Um empréstimo já devolvido não pode ser devolvido novamente.
- Um sócio não pode ter dois empréstimos em aberto do mesmo livro.
