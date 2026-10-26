import re


def validar_nome(nome):
    if not isinstance(nome, str):
        return False

    nome = nome.strip()
    return 2 <= len(nome) <= 120


def validar_idade(idade):
    if isinstance(idade, bool):
        return False

    try:
        idade = int(idade)
    except (TypeError, ValueError):
        return False

    return 1 <= idade <= 120


def validar_telefone(telefone):
    if not isinstance(telefone, str):
        return False

    telefone_limpo = re.sub(r"\D", "", telefone)
    return 10 <= len(telefone_limpo) <= 13


def validar_email(email):
    if not isinstance(email, str):
        return False

    email = email.strip()

    if len(email) > 255:
        return False

    padrao = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"

    if not re.fullmatch(padrao, email):
        return False

    if ".." in email:
        return False

    return True


def validar_senha(senha):
    if not isinstance(senha, str):
        return False

    return len(senha) >= 8 and len(senha) <= 128

