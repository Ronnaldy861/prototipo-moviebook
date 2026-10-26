
from datetime import datetime, timezone

from app.extensions import db


class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    autor = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    sinopse = db.Column(db.Text, nullable=True)
    capa_url = db.Column(db.String(500), nullable=True)
    classificacao = db.Column(db.String(20), nullable=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True)

    criado_em = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    criador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    genero_id = db.Column(
        db.Integer,
        db.ForeignKey("generos.id"),
        nullable=False,
        index=True,
    )

    criador = db.relationship("Usuario", back_populates="livros")
    genero = db.relationship("Genero", back_populates="livros")

    filmes_adaptados = db.relationship(
        "Filme",
        back_populates="livro_origem",
        foreign_keys="Filme.livro_origem_id",
    )

    comentarios = db.relationship(
        "Comentario",
        back_populates="livro",
        foreign_keys="Comentario.livro_id",
    )
    favoritos = db.relationship(
        "Favorito",
        back_populates="livro",
        foreign_keys="Favorito.livro_id",
    )
    avaliacoes = db.relationship(
        "Avaliacao",
        back_populates="livro",
        foreign_keys="Avaliacao.livro_id",
    )

    def __repr__(self):
        return f"<Livro {self.titulo}>"
