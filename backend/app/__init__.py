import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest


from app.extensions import cors, db, migrate


def create_app(test_config=None):
    load_dotenv()

    flask_app = Flask(__name__)

    flask_app.config.from_mapping(
        SECRET_KEY=os.getenv(
            "SECRET_KEY",
            "chave-local-apenas-para-desenvolvimento",
        ),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "sqlite:///moviebook_dev.db",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        flask_app.config.update(test_config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # Registra os modelos no SQLAlchemy.
    import app.models  # noqa: F401

    cors.init_app(
        flask_app,
        resources={
            r"/api/*": {
                "origins": os.getenv(
                    "FRONTEND_ORIGIN",
                    "http://localhost:3000",
                )
            }
        },
    )

    @flask_app.get("/api/health")
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend do MovieBook funcionando.",
        }), 200

    @flask_app.errorhandler(BadRequest)
    def bad_request(_error):
        return jsonify({
            "error": "Requisição inválida.",
        }), 400

    @flask_app.errorhandler(404)
    def not_found(_error):
        return jsonify({
            "error": "Recurso não encontrado.",
        }), 404

    @flask_app.errorhandler(500)
    def internal_server_error(_error):
        return jsonify({
            "error": "Erro interno do servidor.",
        }), 500

    return flask_app
