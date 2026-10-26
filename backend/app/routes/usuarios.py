
from flask import Blueprint, jsonify, request

from app.services.usuarios import cadastrar_usuario


usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.post("/api/usuarios")
def criar_usuario():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie os dados do usuário em formato JSON."
        }), 400

    usuario, erro = cadastrar_usuario(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
        "mensagem": "Usuário cadastrado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "idade": usuario.idade,
            "telefone": usuario.telefone,
            "email": usuario.email,
        },
    }), 201
