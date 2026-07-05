from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.models import models
from app.routers import emprestimos, resumo

# Cria as tabelas automaticamente se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Biblioteca - Empréstimos",
    description="Microsserviço responsável pelo controle de empréstimos e devoluções. "
                 "Consulta o microsserviço catalogo-api para validar livros e sócios.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emprestimos.router)
app.include_router(resumo.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "mensagem": "Serviço de Empréstimos online."
    }
