import os

from flask import Flask, jsonify
from dotenv import load_dotenv

from app.extensions import cors, db, migrate


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "chave-local-apenas-para-desenvolvimento"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "sqlite:///moviebook_dev.db",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": os.getenv(
            "FRONTEND_ORIGIN",
            "http://localhost:3000",
        )}},
    )

    @app.get("/api/health")
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend do MovieBook funcionando.",
        }), 200

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({
            "error": "Recurso não encontrado.",
        }), 404

    @app.errorhandler(500)
    def internal_server_error(_error):
        return jsonify({
            "error": "Erro interno do servidor.",
        }), 500

    return app
