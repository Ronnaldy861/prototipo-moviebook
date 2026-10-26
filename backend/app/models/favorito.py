
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from app.extensions import db


class Favorito(db.Model):
    __tablename__ = "favoritos"

    __table_args__ = (
        CheckConstraint(
            """
            (livro_id IS NOT NULL AND filme_id IS NULL)
            OR
            (livro_id IS NULL AND filme_id IS NOT NULL)
            """,
            name="ck_favorito_uma_obra",
        ),
        UniqueConstraint(
            "usuario_id", "livro_id",
            name="uq_favorito_usuario_livro",
        ),
        UniqueConstraint(
            "usuario_id", "filme_id",
            name="uq_favorito_usuario_filme",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    criado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    livro_id = db.Column(
        db.Integer,
        db.ForeignKey("livros.id"),
        nullable=True,
        index=True,
    )
    filme_id = db.Column(
        db.Integer,
        db.ForeignKey("filmes.id"),
        nullable=True,
        index=True,
    )

    usuario = db.relationship("Usuario", back_populates="favoritos")
    livro = db.relationship("Livro", back_populates="favoritos")
    filme = db.relationship("Filme", back_populates="favoritos")

    def __repr__(self):
        return f"<Favorito {self.id}>"
