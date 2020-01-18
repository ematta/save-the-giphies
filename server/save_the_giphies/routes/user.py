from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import jwt

from save_the_giphies.database.models import Users
from save_the_giphies.config import config
from save_the_giphies.libraries.token import token_required

bp = Blueprint("user", __name__, url_prefix="/user",)


@bp.route("/info", methods=["GET"])
@token_required
def info(user):
    return jsonify({"success": True, "user": user.to_dict()}), 201


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    Users.register(**data)
    return jsonify({"success": True, "message": "Registered user"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.authenticate(**data)
    if not user:
        return jsonify({"message": "Invalid credentials", "authenticated": False}), 401
    token_data = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(token_data, config.secret_key)
    response = {
        "token": token.decode("UTF-8"),
        "user": user.to_dict(),
        "success": True,
        "message": "Registered user",
    }
    return jsonify(response)
