
from datetime import datetime, timezone

from app.extensions import db


class Filme(db.Model):
    __tablename__ = "filmes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False, index=True)
    diretor = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    sinopse = db.Column(db.Text, nullable=True)
    poster_url = db.Column(db.String(500), nullable=True)
    classificacao = db.Column(db.String(20), nullable=True)
    identificador_externo = db.Column(
        db.String(100), unique=True, nullable=True
    )

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
    livro_origem_id = db.Column(
        db.Integer,
        db.ForeignKey("livros.id"),
        nullable=True,
        index=True,
    )

    criador = db.relationship("Usuario", back_populates="filmes")
    genero = db.relationship("Genero", back_populates="filmes")
    livro_origem = db.relationship(
        "Livro",
        back_populates="filmes_adaptados",
        foreign_keys=[livro_origem_id],
    )

    comentarios = db.relationship(
        "Comentario",
        back_populates="filme",
        foreign_keys="Comentario.filme_id",
    )
    favoritos = db.relationship(
        "Favorito",
        back_populates="filme",
        foreign_keys="Favorito.filme_id",
    )
    avaliacoes = db.relationship(
        "Avaliacao",
        back_populates="filme",
        foreign_keys="Avaliacao.filme_id",
    )

    def __repr__(self):
        return f"<Filme {self.titulo}>"
