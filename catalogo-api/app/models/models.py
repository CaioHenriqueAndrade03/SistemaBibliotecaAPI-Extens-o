from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class Livro(Base):
    __tablename__ = "livro"

    id                    = Column(Integer, primary_key=True, index=True)
    titulo                = Column(String(255), nullable=False)
    autor                 = Column(String(255), nullable=False)
    ano_publicacao        = Column(Integer)
    isbn                  = Column(String(20), unique=True)
    quantidade_total      = Column(Integer, nullable=False, default=1)
    quantidade_disponivel = Column(Integer, nullable=False, default=1)

    emprestimos = relationship("Emprestimo", back_populates="livro")

    __table_args__ = (
        CheckConstraint("quantidade_total >= 0",      name="ck_livro_qtd_total"),
        CheckConstraint("quantidade_disponivel >= 0", name="ck_livro_qtd_disp"),
    )


class Socio(Base):
    __tablename__ = "socio"

    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(255), nullable=False)
    email         = Column(String(255), unique=True, nullable=False)
    telefone      = Column(String(20))
    data_cadastro = Column(Date, nullable=False)

    emprestimos = relationship("Emprestimo", back_populates="socio")


class Emprestimo(Base):
    __tablename__ = "emprestimo"

    id                      = Column(Integer, primary_key=True, index=True)
    livro_id                = Column(Integer, ForeignKey("livro.id"), nullable=False)
    socio_id                = Column(Integer, ForeignKey("socio.id"), nullable=False)
    data_emprestimo         = Column(Date, nullable=False)
    data_prevista_devolucao = Column(Date, nullable=False)
    data_devolucao          = Column(Date, nullable=True)
    status                  = Column(String(20), nullable=False, default="aberto")

    livro = relationship("Livro", back_populates="emprestimos")
    socio = relationship("Socio", back_populates="emprestimos")

    __table_args__ = (
        CheckConstraint("status IN ('aberto', 'devolvido')", name="ck_emprestimo_status"),
    )
