# Sistema de Biblioteca

Sistema distribuído de gestão de biblioteca, dividido em **2 microsserviços** (catálogo e empréstimos), cada um com sua própria API REST e seu próprio banco de dados, desenvolvidos com **FastAPI + PostgreSQL** e orquestrados via Docker Compose.

Projeto de extensão relacionado ao **ODS 4 — Educação de Qualidade**, da ONU.

---

## Tecnologias utilizadas

| Camada       | Tecnologia                  |
|--------------|-----------------------------|
| Linguagem    | Python 3.12                 |
| Framework    | FastAPI                     |
| ORM          | SQLAlchemy 2.0              |
| Comunicação entre serviços | HTTP (httpx)  |
| Banco        | PostgreSQL 16 (um banco por serviço) |
| Containers   | Docker + Docker Compose     |
| CI/CD        | GitHub Actions              |
| Editor       | VSCode                      |

---

## Arquitetura do projeto

O sistema é composto por dois microsserviços independentes, cada um com seu próprio banco de dados, que se comunicam entre si via HTTP:

- **`catalogo-api`** — responsável pelo cadastro e consulta de livros e sócios.
- **`emprestimos-api`** — responsável pelos empréstimos, devoluções e resumo geral. Consulta o `catalogo-api` via HTTP para validar livros/sócios e ajustar o estoque disponível.

O frontend (repositório separado: [SistemaBibliotecaFrontend](https://github.com/DrTavinho/SistemaBibliotecaFrontend)) consome as duas APIs diretamente.

<img width="565" height="410" alt="Diagrama de arquitetura do sistema" src="https://github.com/user-attachments/assets/65155e73-3f4e-4783-92dc-e8f0a8e55435" />

---

## Estrutura do projeto

```
SistemaBibliotecaAPI-Extensão/
├── .github/
│   └── workflows/
│       └── ci.yml         # Pipeline de CI/CD (testes automáticos)
├── catalogo-api/
│   ├── app/
│   │   ├── db/           # Conexão com o banco (SQLAlchemy)
│   │   ├── models/       # Modelos das tabelas (Livro, Sócio, Empréstimo)
│   │   ├── routers/      # Rotas da API (livros, socios)
│   │   └── schemas/      # Schemas Pydantic (validação de entrada/saída)
│   ├── tests/
│   │   └── test_health.py
│   ├── sql/
│   │   └── init.sql
│   ├── config.py
│   ├── main.py
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── requirements.txt
│   └── .env.example
├── emprestimos-api/
│   ├── app/
│   │   ├── db/           # Conexão com o banco próprio (SQLAlchemy)
│   │   ├── models/       # Modelo de Empréstimo
│   │   ├── routers/      # Rotas da API (emprestimos, resumo)
│   │   ├── schemas/      # Schemas Pydantic
│   │   └── clients/      # Cliente HTTP para se comunicar com o catalogo-api
│   ├── tests/
│   │   └── test_health.py
│   ├── config.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── .gitattributes
├── .env.example               # Variáveis de ambiente dos 2 bancos (produção)
├── docker-compose.yml         # Ambiente de desenvolvimento
├── docker-compose.prod.yml    # Ambiente de produção
└── README.md
```

> O frontend não faz parte deste repositório — ele está em [SistemaBibliotecaFrontend](https://github.com/DrTavinho/SistemaBibliotecaFrontend).

---

## Como executar em desenvolvimento

```bash
# 1. Clone o projeto e entre na pasta
cd SistemaBibliotecaAPI-Extensão

# 2. Suba os containers dos dois microsserviços e seus bancos
docker compose up --build

# 3. Acesse a documentação interativa de cada serviço
# catalogo-api:    http://localhost:8000/docs
# emprestimos-api: http://localhost:8001/docs
```

O `docker compose` sobe 4 containers: `db_catalogo`, `catalogo-api`, `db_emprestimos` e `emprestimos-api`. Confirme com:

```bash
docker ps
```

---

## Como executar em produção

```bash
# 1. Crie o arquivo .env na raiz do projeto, a partir do exemplo
cp .env.example .env

# 2. Edite o .env com senhas seguras para os dois bancos

# 3. Suba com o compose de produção
docker compose -f docker-compose.prod.yml up --build -d
```

O `docker-compose.prod.yml` já está atualizado para orquestrar os dois microsserviços, cada um com seu próprio banco PostgreSQL e variáveis de ambiente próprias (veja `.env.example` na raiz).

---

## Portas utilizadas

| Serviço          | Porta (host) | Descrição                     |
|------------------|--------------|--------------------------------|
| catalogo-api     | 8000         | API REST (livros e sócios)     |
| emprestimos-api  | 8001         | API REST (empréstimos e resumo)|
| db_catalogo      | 5433         | PostgreSQL do catalogo-api     |
| db_emprestimos   | 5434         | PostgreSQL do emprestimos-api  |

---

## Endpoints principais

### Livros (`catalogo-api`)
| Método | Rota                       | Descrição                                    |
|--------|-----------------------------|-----------------------------------------------|
| POST   | `/livros/`                 | Cadastra um livro                              |
| GET    | `/livros/`                 | Lista todos os livros                          |
| GET    | `/livros/disponiveis`      | Lista livros com estoque > 0                   |
| GET    | `/livros/{id}`             | Busca livro por ID                             |
| PATCH  | `/livros/{id}/estoque`     | Ajusta a quantidade disponível (uso interno, chamado pelo emprestimos-api) |

### Sócios (`catalogo-api`)
| Método | Rota           | Descrição              |
|--------|----------------|-------------------------|
| POST   | `/socios/`     | Cadastra um sócio       |
| GET    | `/socios/`     | Lista todos os sócios   |
| GET    | `/socios/{id}` | Busca sócio por ID      |

### Empréstimos (`emprestimos-api`)
| Método | Rota                          | Descrição                    |
|--------|-------------------------------|--------------------------------|
| POST   | `/emprestimos/`              | Efetua um empréstimo (valida livro/sócio e reserva estoque via catalogo-api) |
| PATCH  | `/emprestimos/{id}/devolver` | Registra devolução (libera estoque via catalogo-api) |
| GET    | `/emprestimos/`              | Lista todos os empréstimos     |
| GET    | `/emprestimos/abertos`       | Lista empréstimos em aberto    |

### Resumo (`emprestimos-api`)
| Método | Rota       | Descrição                                                        |
|--------|------------|--------------------------------------------------------------------|
| GET    | `/resumo/` | Total de livros e sócios (via catalogo-api) + empréstimos em aberto |

---

## Exemplos de uso

### Cadastrar um livro (`catalogo-api`, porta 8000)
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

### Cadastrar um sócio (`catalogo-api`, porta 8000)
```json
POST /socios/
{
  "nome": "Ana Souza",
  "email": "ana@email.com",
  "telefone": "11999990000"
}
```

### Efetuar um empréstimo (`emprestimos-api`, porta 8001)
```json
POST /emprestimos/
{
  "livro_id": 1,
  "socio_id": 1,
  "data_prevista_devolucao": "2026-06-10"
}
```

### Devolver um livro (`emprestimos-api`, porta 8001)
```
PATCH /emprestimos/1/devolver
(sem corpo — apenas o ID na URL)
```

---

## Regras de negócio

- Um livro só pode ser emprestado se houver ao menos 1 exemplar disponível (validado via chamada HTTP ao `catalogo-api`).
- Ao efetuar empréstimo, `quantidade_disponivel` é decrementada no `catalogo-api` através do endpoint `PATCH /livros/{id}/estoque`.
- Ao devolver, `quantidade_disponivel` é incrementada da mesma forma.
- Um empréstimo já devolvido não pode ser devolvido novamente.
- Um sócio não pode ter dois empréstimos em aberto do mesmo livro.

---

## CI/CD

O repositório possui um pipeline no GitHub Actions (`.github/workflows/ci.yml`) que instala as dependências e roda os testes de saúde dos dois microsserviços a cada push na branch `main`.

---

## Segurança e LGPD

O sistema processa dados pessoais de sócios (nome, contato e histórico de empréstimos). A versão atual **não possui autenticação implementada**, funcionando como protótipo acadêmico. Para produção, seriam necessários JWT, hash de senhas, HTTPS e políticas de retenção/exclusão de dados conforme a LGPD.