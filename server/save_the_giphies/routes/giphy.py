from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphies
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required
from typing import TYPE_CHECKING, Tuple, List, Dict

if TYPE_CHECKING:
    from flask.wrappers import Response

bp = Blueprint("giphy", __name__, url_prefix="/giphy",)


@bp.route("/search", methods=["POST"])
def search_all_giphies() -> "Tuple[Response, int]":
    """Retrieves all giphies (no user association)

    Returns Tuple[Response, int]
    """
    response: "List[Dict]" = retriever.retrieve_giphies(**request.get_json())
    success: "int" = 200 if len(response) > 0 else 404
    return jsonify(response), success

@bp.route("/search/<string:giphy_id>", methods=["GET"])
def delete_user_giphy(giphy_id: "str") -> "Tuple[Response, int]":
    """ Deletes giphy from user account
    Params:
        giphy (str): Giphy ID provided by GIPHY

    Returns Tuple[Response, int]
    """
    response: "List[Dict]" = retriever.retrieve_giphy(giphy_id=giphy_id)
    status: "int" = 201 if response else 404
    return jsonify(response), status
