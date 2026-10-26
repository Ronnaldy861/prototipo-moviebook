from app import create_app


def test_rota_health():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    cliente = app.test_client()
    resposta = cliente.get("/api/health")

    assert resposta.status_code == 200
    assert resposta.json["status"] == "ok"


def test_rota_inexistente():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    cliente = app.test_client()
    resposta = cliente.get("/api/rota-inexistente")

    assert resposta.status_code == 404
    assert resposta.json["error"] == "Recurso não encontrado."