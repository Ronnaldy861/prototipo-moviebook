
from datetime import datetime, timezone

from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    livros = db.relationship("Livro", back_populates="criador")
    filmes = db.relationship("Filme", back_populates="criador")
    comentarios = db.relationship(
        "Comentario", back_populates="usuario", cascade="all, delete-orphan"
    )
    favoritos = db.relationship(
        "Favorito", back_populates="usuario", cascade="all, delete-orphan"
    )
    avaliacoes = db.relationship(
        "Avaliacao", back_populates="usuario", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario {self.id}: {self.email}>"
