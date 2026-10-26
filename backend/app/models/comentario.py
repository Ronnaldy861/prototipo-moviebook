
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint

from app.extensions import db


class Comentario(db.Model):
    __tablename__ = "comentarios"

    __table_args__ = (
        CheckConstraint(
            """
            (livro_id IS NOT NULL AND filme_id IS NULL)
            OR
            (livro_id IS NULL AND filme_id IS NOT NULL)
            """,
            name="ck_comentario_uma_obra",
        ),
        CheckConstraint(
            "length(trim(texto)) BETWEEN 1 AND 2000",
            name="ck_comentario_texto_valido",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
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

    usuario = db.relationship("Usuario", back_populates="comentarios")
    livro = db.relationship("Livro", back_populates="comentarios")
    filme = db.relationship("Filme", back_populates="comentarios")

    def __repr__(self):
        return f"<Comentario {self.id}>"
