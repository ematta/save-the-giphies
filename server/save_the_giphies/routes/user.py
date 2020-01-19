from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import jwt

from save_the_giphies.database.models import Users
from save_the_giphies.config import config
from save_the_giphies.libraries.token import token_required

from typing import Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from flask.wrappers import Response

bp = Blueprint("user", __name__, url_prefix="/user",)


@bp.route("/register", methods=["POST"])
def register() -> "Tuple[Response, int]":
    """Register user (payload in response.get_json() which has name, email, and password)

    Returns Tuple[Response, int]
    """
    data: "Dict" = request.get_json()
    result: "Dict" = Users.register(**data)
    status: "int" = 201 if result["success"] else 501
    return jsonify({"success": result["success"], "msg": result["msg"]}), status


@bp.route("/login", methods=["POST"])
def login():
    """Register user (payload in response.get_json() which has email and password)

    Returns Tuple[Response, int]
    """
    data: "Dict" = request.get_json()
    result: "Dict" = Users.authenticate(**data)
    if not result["success"]:
        return jsonify({"msg": result["msg"], "authenticated": False}), 401
    user: "Users" = result["user"]
    token_data = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token: "bytes" = jwt.encode(token_data, config.secret_key)
    response: "Dict" = {
        "token": token.decode("UTF-8"),
        "user": user.to_dict(),
        "success": True,
        "msg": "Registered user",
    }
    return jsonify(response), 200


@bp.route("/info", methods=["GET"])
@token_required
def info(user: "Users") -> "Tuple[Response, int]":
    """Get user from token_require
    Params:
        user (Users): User model provided by token_required

    Returns Tuple[Response, int]
    """
    return jsonify({"success": True, "user": user.to_dict()}), 200
