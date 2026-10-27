
from app import create_app


def criar_app_teste():
    return create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })


def test_rota_health():
    app = criar_app_teste()

    cliente = app.test_client()
    resposta = cliente.get("/api/health")

    assert resposta.status_code == 200
    assert resposta.json["status"] == "ok"


def test_rota_inexistente():
    app = criar_app_teste()

    cliente = app.test_client()
    resposta = cliente.get("/api/rota-inexistente")

    assert resposta.status_code == 404
    assert resposta.json["error"] == "Recurso não encontrado."


def test_cadastro_sem_json():
    app = criar_app_teste()

    cliente = app.test_client()
    resposta = cliente.post("/api/usuarios")

    assert resposta.status_code == 400
    assert resposta.json["erro"] == (
        "Envie os dados do usuário em formato JSON."
    )


def test_cadastro_usuario_valido():
    from app.extensions import db
    from app.models import Usuario

    app = criar_app_teste()

    with app.app_context():
        db.create_all()

        try:
            cliente = app.test_client()
            resposta = cliente.post(
                "/api/usuarios",
                json={
                    "nome": "Usuario Teste",
                    "idade": 18,
                    "telefone": "84999999999",
                    "email": "usuario.teste@example.com",
                    "senha": "SenhaTeste123",
                },
            )

            assert resposta.status_code == 201
            assert resposta.json["mensagem"] == (
                "Usuário cadastrado com sucesso."
            )
            assert "senha" not in resposta.json["usuario"]

            usuario = db.session.execute(
                db.select(Usuario).where(
                    Usuario.email == "usuario.teste@example.com"
                )
            ).scalar_one()

            assert usuario.senha_hash != "SenhaTeste123"
        finally:
            db.session.remove()
            db.drop_all()


def test_cadastro_email_duplicado():
    from app.extensions import db

    app = criar_app_teste()

    with app.app_context():
        db.create_all()

        dados = {
            "nome": "Usuario Teste",
            "idade": 18,
            "telefone": "84999999999",
            "email": "duplicado@example.com",
            "senha": "SenhaTeste123",
        }

        try:
            cliente = app.test_client()

            primeira_resposta = cliente.post(
                "/api/usuarios",
                json=dados,
            )

            segunda_resposta = cliente.post(
                "/api/usuarios",
                json=dados,
            )

            assert primeira_resposta.status_code == 201
            assert segunda_resposta.status_code == 400
            assert segunda_resposta.json["erro"] == (
                "Não foi possível cadastrar com esse e-mail."
            )
        finally:
            db.session.remove()
            db.drop_all()


def test_cadastro_com_email_invalido():
    app = criar_app_teste()

    cliente = app.test_client()
    resposta = cliente.post(
        "/api/usuarios",
        json={
            "nome": "Usuario Teste",
            "idade": 18,
            "telefone": "84999999999",
            "email": "email-invalido",
            "senha": "SenhaTeste123",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json["erro"] == "Informe um e-mail válido."


def test_cadastro_com_senha_curta():
    app = criar_app_teste()

    cliente = app.test_client()
    resposta = cliente.post(
        "/api/usuarios",
        json={
            "nome": "Usuario Teste",
            "idade": 18,
            "telefone": "84999999999",
            "email": "senha.curta@example.com",
            "senha": "123",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json["erro"] == (
        "A senha deve ter entre 8 e 128 caracteres."
    )
