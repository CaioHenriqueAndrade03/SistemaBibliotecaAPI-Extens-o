from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Emprestimo, Livro, Socio
from app.schemas.schemas import EmprestimoCreate, EmprestimoOut
from typing import List
from datetime import date

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post("/", response_model=EmprestimoOut, status_code=201)
def efetuar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    """
    Realiza um empréstimo.
    Regras de negócio:
    - Livro e sócio devem existir.
    - Livro deve ter ao menos 1 exemplar disponível.
    - Sócio não pode ter empréstimo em aberto do mesmo livro.
    """
    # Verifica existência do livro
    livro = db.query(Livro).filter(Livro.id == dados.livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Verifica existência do sócio
    socio = db.query(Socio).filter(Socio.id == dados.socio_id).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Sócio não encontrado.")

    # Regra: livro deve ter exemplar disponível
    if livro.quantidade_disponivel < 1:
        raise HTTPException(
            status_code=400,
            detail=f"Não há exemplares disponíveis de '{livro.titulo}'."
        )

    # Regra: sócio não pode ter empréstimo em aberto do mesmo livro
    emprestimo_aberto = db.query(Emprestimo).filter(
        Emprestimo.livro_id == dados.livro_id,
        Emprestimo.socio_id == dados.socio_id,
        Emprestimo.status == "aberto",
    ).first()
    if emprestimo_aberto:
        raise HTTPException(
            status_code=400,
            detail="Sócio já possui um empréstimo em aberto deste livro."
        )

    # Cria o empréstimo e diminui a quantidade disponível
    novo = Emprestimo(
        livro_id=dados.livro_id,
        socio_id=dados.socio_id,
        data_emprestimo=date.today(),
        data_prevista_devolucao=dados.data_prevista_devolucao,
        status="aberto",
    )
    livro.quantidade_disponivel -= 1

    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.patch("/{emprestimo_id}/devolver", response_model=EmprestimoOut)
def devolver_livro(emprestimo_id: int, db: Session = Depends(get_db)):
    """
    Registra a devolução de um livro.
    Regras de negócio:
    - Empréstimo deve existir.
    - Empréstimo não pode já estar devolvido.
    - Incrementa a quantidade disponível do livro.
    """
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    # Regra: não pode devolver duas vezes
    if emprestimo.status == "devolvido":
        raise HTTPException(
            status_code=400,
            detail="Este empréstimo já foi devolvido."
        )

    # Registra devolução e incrementa estoque
    emprestimo.status = "devolvido"
    emprestimo.data_devolucao = date.today()
    emprestimo.livro.quantidade_disponivel += 1

    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.get("/", response_model=List[EmprestimoOut])
def listar_emprestimos(db: Session = Depends(get_db)):
    """Lista todos os empréstimos."""
    return db.query(Emprestimo).all()


@router.get("/abertos", response_model=List[EmprestimoOut])
def listar_emprestimos_abertos(db: Session = Depends(get_db)):
    """Lista apenas os empréstimos ainda em aberto."""
    return db.query(Emprestimo).filter(Emprestimo.status == "aberto").all()


@router.get("/{emprestimo_id}", response_model=EmprestimoOut)
def buscar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    """Busca um empréstimo pelo ID."""
    emp = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")
    return emp
