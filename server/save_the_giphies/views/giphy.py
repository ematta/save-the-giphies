from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphy
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required

bp = Blueprint("giphy", __name__, url_prefix="/giphy",)


@bp.route("/search", methods=["POST"])
def search():
    response = retriever.retrieve_giphies(**request.get_json())
    return jsonify(response)


@bp.route("/get/<user_id>", methods=["GET"])
@token_required
def getUserGiphies(user_id):
    all_giphies = Giphy.all_giphies(user=user_id)
    return jsonify([giphy.to_dict() for giphy in all_giphies])


@bp.route("/set/<user_id>", methods=["POST"])
@token_required
def setUserGiphy(user_id):
    data = request.get_json()
    giphy = Giphy(user=user_id, giphy=data.giphy)
    return jsonify(giphy.to_dict()), 201
