from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmprestimoCreate(BaseModel):
    livro_id: int
    socio_id: int
    data_prevista_devolucao: date


class EmprestimoOut(BaseModel):
    id: int
    livro_id: int
    socio_id: int
    data_emprestimo: date
    data_prevista_devolucao: date
    data_devolucao: Optional[date] = None
    status: str

    class Config:
        from_attributes = True
