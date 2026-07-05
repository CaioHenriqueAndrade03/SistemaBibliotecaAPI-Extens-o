from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Emprestimo
from app.clients import catalogo_client
from pydantic import BaseModel

router = APIRouter(prefix="/resumo", tags=["Resumo"])


class ResumoOut(BaseModel):
    total_livros: int
    total_socios: int
    emprestimos_em_aberto: int


@router.get("/", response_model=ResumoOut)
def resumo(db: Session = Depends(get_db)):
    """
    Retorna um resumo geral do sistema, agregando dados dos dois microsserviços:
    total_livros e total_socios vêm do catalogo-api (via HTTP);
    emprestimos_em_aberto vem do banco local deste serviço.
    """
    return ResumoOut(
        total_livros=catalogo_client.contar_livros(),
        total_socios=catalogo_client.contar_socios(),
        emprestimos_em_aberto=db.query(Emprestimo).filter(
            Emprestimo.status == "aberto"
        ).count(),
    )
