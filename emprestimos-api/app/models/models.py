from sqlalchemy import Column, Integer, Date, String
from app.db.database import Base


class Emprestimo(Base):
    """
    Representa um empréstimo.

    Diferente da versão monolítica, este modelo NÃO tem foreign key
    para Livro/Socio, pois essas entidades agora vivem no microsserviço
    catalogo-api. Guardamos apenas os IDs (livro_id, socio_id) e validamos
    sua existência via chamada HTTP ao catalogo-api (ver app/clients).
    """
    __tablename__ = "emprestimos"

    id = Column(Integer, primary_key=True, index=True)
    livro_id = Column(Integer, nullable=False, index=True)
    socio_id = Column(Integer, nullable=False, index=True)
    data_emprestimo = Column(Date, nullable=False)
    data_prevista_devolucao = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="aberto")  # "aberto" | "devolvido"
