from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.db.database import get_db

# ─────────────────────────────────────────────
# Livro
# ─────────────────────────────────────────────

class LivroCreate(BaseModel):
    titulo:           str
    autor:            str
    ano_publicacao:   Optional[int]  = None
    isbn:             Optional[str]  = None
    quantidade_total: int            = 1


class LivroOut(BaseModel):
    id:                    int
    titulo:                str
    autor:                 str
    ano_publicacao:        Optional[int]
    isbn:                  Optional[str]
    quantidade_total:      int
    quantidade_disponivel: int

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Sócio
# ─────────────────────────────────────────────

class SocioCreate(BaseModel):
    nome:     str
    email:    EmailStr
    telefone: Optional[str] = None


class SocioOut(BaseModel):
    id:            int
    nome:          str
    email:         str
    telefone:      Optional[str]
    data_cadastro: date

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Empréstimo
# ─────────────────────────────────────────────

class EmprestimoCreate(BaseModel):
    livro_id:               int
    socio_id:               int
    data_prevista_devolucao: date


class EmprestimoOut(BaseModel):
    id:                      int
    livro_id:                int
    socio_id:                int
    data_emprestimo:         date
    data_prevista_devolucao: date
    data_devolucao:          Optional[date]
    status:                  str

    model_config = {"from_attributes": True}
