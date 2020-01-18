from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphies
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from flask.wrappers import Response

bp = Blueprint("giphy", __name__, url_prefix="/giphy",)


@bp.route("/search", methods=["POST"])
def search_all_giphies() -> "Tuple[Response, int]":
    response = retriever.retrieve_giphies(**request.get_json())
    return jsonify(response), 200


@bp.route("/user", methods=["GET"])
@token_required
def get_user_giphies(user):
    all_giphies = Giphies.all_giphies(users_id=user.id)
    results = [
        retriever.retrieve_giphy(giphy.to_dict()["giphy"]) for giphy in all_giphies
    ]
    return jsonify(results)


@bp.route("/user/<giphy>", methods=["DELETE"])
@token_required
def delete_user_giphy(user, giphy):
    Giphies.delete_giphy(users_id=user.id, giphy=giphy)
    return jsonify({"success": True}), 204


@bp.route("/user/<giphy>", methods=["POST"])
@token_required
def save_user_giphy(user, giphy):
    try:
        Giphies.save_giphy(users_id=user.id, giphy=giphy)
        return jsonify({"success": True, "message": "Saved giphy"}), 201
    except Exception:
        return jsonify({"success": False, "message": "Already in your profile"}), 405
