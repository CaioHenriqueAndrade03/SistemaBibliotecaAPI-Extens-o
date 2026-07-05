from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Livro, Socio, Emprestimo
from pydantic import BaseModel

router = APIRouter(prefix="/resumo", tags=["Resumo"])


class ResumoOut(BaseModel):
    total_livros:           int
    total_socios:           int
    emprestimos_em_aberto:  int


@router.get("/", response_model=ResumoOut)
def resumo(db: Session = Depends(get_db)):
    """Retorna um resumo geral do sistema."""
    return ResumoOut(
        total_livros=db.query(Livro).count(),
        total_socios=db.query(Socio).count(),
        emprestimos_em_aberto=db.query(Emprestimo).filter(
            Emprestimo.status == "aberto"
        ).count(),
    )
