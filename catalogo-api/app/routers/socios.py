from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Socio
from app.schemas.schemas import SocioCreate, SocioOut
from typing import List
from datetime import date

router = APIRouter(prefix="/socios", tags=["Sócios"])


@router.post("/", response_model=SocioOut, status_code=201)
def cadastrar_socio(socio: SocioCreate, db: Session = Depends(get_db)):
    """Cadastra um novo sócio na biblioteca."""
    # Verifica e-mail duplicado
    existente = db.query(Socio).filter(Socio.email == socio.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    novo = Socio(
        nome=socio.nome,
        email=socio.email,
        telefone=socio.telefone,
        data_cadastro=date.today(),
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=List[SocioOut])
def listar_socios(db: Session = Depends(get_db)):
    """Lista todos os sócios cadastrados."""
    return db.query(Socio).all()


@router.get("/{socio_id}", response_model=SocioOut)
def buscar_socio(socio_id: int, db: Session = Depends(get_db)):
    """Busca um sócio pelo ID."""
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Sócio não encontrado.")
    return socio
