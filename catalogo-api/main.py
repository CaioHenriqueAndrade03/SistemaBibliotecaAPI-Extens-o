from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.models import models
from app.routers import livros, socios, emprestimos, resumo

# Cria as tabelas automaticamente se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Biblioteca",
    description="API para controle de livros, sócios e empréstimos.",
    version="1.0.0",
)

# Configuração CORS
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

# Registra os roteadores
app.include_router(livros.router)
app.include_router(socios.router)
app.include_router(emprestimos.router)
app.include_router(resumo.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "mensagem": "Sistema de Biblioteca online."
    }