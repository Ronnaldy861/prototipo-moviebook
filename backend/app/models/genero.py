
from app.extensions import db


class Genero(db.Model):
    __tablename__ = "generos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), unique=True, nullable=False)

    livros = db.relationship("Livro", back_populates="genero")
    filmes = db.relationship("Filme", back_populates="genero")

    def __repr__(self):
        return f"<Genero {self.nome}>"
