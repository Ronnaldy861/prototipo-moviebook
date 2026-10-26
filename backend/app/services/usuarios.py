
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Usuario
from app.services.validacoes import (
    validar_email,
    validar_idade,
    validar_nome,
    validar_senha,
    validar_telefone,
)


def cadastrar_usuario(dados):
    if not isinstance(dados, dict):
        return None, "Os dados enviados são inválidos."

    nome = dados.get("nome")
    idade = dados.get("idade")
    telefone = dados.get("telefone")
    email = dados.get("email")
    senha = dados.get("senha")

    if not validar_nome(nome):
        return None, "Informe um nome entre 2 e 120 caracteres."

    if not validar_idade(idade):
        return None, "Informe uma idade válida."

    if not validar_telefone(telefone):
        return None, "Informe um telefone válido."

    if not validar_email(email):
        return None, "Informe um e-mail válido."

    if not validar_senha(senha):
        return None, "A senha deve ter entre 8 e 128 caracteres."

    nome = nome.strip()
    email = email.strip().lower()
    telefone = telefone.strip()
    idade = int(idade)

    usuario_existente = db.session.execute(
        db.select(Usuario).where(Usuario.email == email)
    ).scalar_one_or_none()

    if usuario_existente:
        return None, "Não foi possível cadastrar com esse e-mail."

    usuario = Usuario(
        nome=nome,
        idade=idade,
        telefone=telefone,
        email=email,
        senha_hash=generate_password_hash(senha),
    )

    try:
        db.session.add(usuario)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return usuario, None
