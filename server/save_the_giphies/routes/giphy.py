from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphies
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required
from typing import TYPE_CHECKING, Tuple, List, Dict

if TYPE_CHECKING:
    from flask.wrappers import Response
    from save_the_giphies.database.models import Users

bp = Blueprint("giphy", __name__, url_prefix="/giphy",)


@bp.route("/search", methods=["POST"])
def search_all_giphies() -> "Tuple[Response, int]":
    """Retrieves all giphies (no user association)

    Returns Tuple[Response, int]
    """
    response: "List[Dict]" = retriever.retrieve_giphies(**request.get_json())
    success: "int" = 200 if len(response) > 0 else 404
    return jsonify(response), success


@bp.route("/user", methods=["GET"])
@token_required
def get_user_giphies_call(user: "Users") -> "Tuple[Response, int]":
    return get_user_giphies(user)


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


@bp.route("/user/<string:giphy>", methods=["DELETE"])
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


@bp.route("/user/<string:giphy>", methods=["POST"])
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
