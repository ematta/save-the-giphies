from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import jwt

from save_the_giphies.database.models import Users, Giphies
from save_the_giphies.config import config
from save_the_giphies.libraries.token import token_required
from save_the_giphies.libraries.retriever import retriever

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



@bp.route("/giphy", methods=["GET"])
@token_required
def get_user_giphies(user: "Users") -> "Tuple[Response, int]":
    """ Retrieves giphies associated with Account
    Params:
        user (Users): User model provided by token_required

    Returns Tuple[Response, int]
    """
    all_giphies: "List[Giphies]" = Giphies.all_giphies(users_id=user.id)
    results: "List[Dict]" = [
        retriever.retrieve_giphy(giphy.to_dict()["giphy"]) for giphy in all_giphies
    ]
    return jsonify(results), 200

@bp.route("/giphy/<string:giphy>", methods=["DELETE"])
@token_required
def delete_user_giphy(user: "Users", giphy: "str") -> "Tuple[Response, int]":
    """ Deletes giphy from user account
    Params:
        user (Users): User model provided by token_required
        giphy (str): Giphy ID provided by GIPHY

    Returns Tuple[Response, int]
    """
    success: "bool" = Giphies.delete_giphy(users_id=user.id, giphy=giphy)
    status: "int" = 201 if success else 404
    return jsonify({"success": success}), status


@bp.route("/giphy/<string:giphy>", methods=["POST"])
@token_required
def save_user_giphy(user: "Users", giphy: "str") -> "Tuple[Response, int]":
    """ Saves giphy to user account
    Params:
        user (Users): User model provided by token_required
        giphy (str): Giphy ID provided by GIPHY

    Returns Tuple[Response, int]
    """
    results: "Dict" = Giphies.save_giphy(users_id=user.id, giphy=giphy)
    status: "int" = 201 if results["success"] else 405
    return jsonify({"success": results["success"], "msg": results["msg"]}), status
