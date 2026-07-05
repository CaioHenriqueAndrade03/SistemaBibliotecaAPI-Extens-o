from pydantic import BaseModel
from app.db.database import get_db

class EstoqueUpdate(BaseModel):
    delta: int  # -1 para reservar exemplar (empréstimo), +1 para devolver


@router.patch("/{livro_id}/estoque", response_model=LivroOut)
def ajustar_estoque(livro_id: int, dados: EstoqueUpdate, db: Session = Depends(get_db)):
    """
    Ajusta a quantidade de exemplares disponíveis de um livro.
    Usado pelo microsserviço de empréstimos para reservar (delta=-1)
    ou liberar (delta=+1) um exemplar, mantendo a consistência
    entre os dois serviços sem que eles compartilhem o mesmo banco.
    """
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    nova_quantidade = livro.quantidade_disponivel + dados.delta
    if nova_quantidade < 0:
        raise HTTPException(
            status_code=400,
            detail="Não há exemplares disponíveis suficientes para este ajuste."
        )
    if nova_quantidade > livro.quantidade_total:
        raise HTTPException(
            status_code=400,
            detail="Ajuste ultrapassaria a quantidade total de exemplares."
        )

    livro.quantidade_disponivel = nova_quantidade
    db.commit()
    db.refresh(livro)
    return livro