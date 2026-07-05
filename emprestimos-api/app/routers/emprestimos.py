from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Emprestimo
from app.schemas.schemas import EmprestimoCreate, EmprestimoOut
from app.clients import catalogo_client
from typing import List
from datetime import date

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post("/", response_model=EmprestimoOut, status_code=201)
def efetuar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    """
    Realiza um empréstimo.
    Regras de negócio:
    - Livro e sócio devem existir (validado via catalogo-api).
    - Livro deve ter ao menos 1 exemplar disponível (validado via catalogo-api).
    - Sócio não pode ter empréstimo em aberto do mesmo livro (validado neste serviço).
    """
    # Verifica existência e disponibilidade do livro no catalogo-api
    livro = catalogo_client.buscar_livro(dados.livro_id)
    if livro["quantidade_disponivel"] < 1:
        raise HTTPException(
            status_code=400,
            detail=f"Não há exemplares disponíveis de '{livro['titulo']}'."
        )

    # Verifica existência do sócio no catalogo-api
    catalogo_client.buscar_socio(dados.socio_id)

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

    # Cria o empréstimo localmente
    novo = Emprestimo(
        livro_id=dados.livro_id,
        socio_id=dados.socio_id,
        data_emprestimo=date.today(),
        data_prevista_devolucao=dados.data_prevista_devolucao,
        status="aberto",
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    # Só reserva o exemplar no catalogo-api depois de confirmar o registro local
    catalogo_client.ajustar_estoque(dados.livro_id, delta=-1)

    return novo


@router.patch("/{emprestimo_id}/devolver", response_model=EmprestimoOut)
def devolver_livro(emprestimo_id: int, db: Session = Depends(get_db)):
    """
    Registra a devolução de um livro.
    Regras de negócio:
    - Empréstimo deve existir.
    - Empréstimo não pode já estar devolvido.
    - Incrementa a quantidade disponível do livro via catalogo-api.
    """
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    if emprestimo.status == "devolvido":
        raise HTTPException(
            status_code=400,
            detail="Este empréstimo já foi devolvido."
        )

    emprestimo.status = "devolvido"
    emprestimo.data_devolucao = date.today()
    db.commit()
    db.refresh(emprestimo)

    # Libera o exemplar de volta no catalogo-api
    catalogo_client.ajustar_estoque(emprestimo.livro_id, delta=1)

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
