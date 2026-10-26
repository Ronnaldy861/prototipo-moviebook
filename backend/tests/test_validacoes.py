from app.services.validacoes import (
    validar_email,
    validar_idade,
    validar_nome,
    validar_senha,
    validar_telefone,
)


def test_validar_nome():
    assert validar_nome("Ronnaldy")
    assert not validar_nome("")
    assert not validar_nome("A")
    assert not validar_nome(None)


def test_validar_idade():
    assert validar_idade(18)
    assert validar_idade("18")
    assert not validar_idade(0)
    assert not validar_idade(121)
    assert not validar_idade("idade")
    assert not validar_idade(True)


def test_validar_telefone():
    assert validar_telefone("(84) 99999-9999")
    assert validar_telefone("84999999999")
    assert not validar_telefone("123")
    assert not validar_telefone(None)


def test_validar_email():
    assert validar_email("usuario@example.com")
    assert not validar_email("email-invalido")
    assert not validar_email("usuario@")
    assert not validar_email("usuario..teste@example.com")
    assert not validar_email(None)


def test_validar_senha():
    assert validar_senha("senha123")
    assert not validar_senha("123")
    assert not validar_senha("")
    assert not validar_senha(None)
    assert not validar_senha("a" * 129)
