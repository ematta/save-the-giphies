from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphy
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required
from save_the_giphies.database.engine import db_session

bp = Blueprint("giphy", __name__, url_prefix="/giphy",)


@bp.route("/search", methods=["POST"])
def search_all_giphies():
    response = retriever.retrieve_giphies(**request.get_json())
    return jsonify(response)


@bp.route("/user", methods=["GET"])
@token_required
def get_user_giphies(user):
    all_giphies = Giphy.all_giphies(user_id=user.id)
    results = [
        retriever.retrieve_giphy(giphy.to_dict()['giphy'])
        for giphy
        in all_giphies
    ]
    return jsonify(results)

@bp.route("/user/<giphy>", methods=["DELETE"])
@token_required
def delete_user_giphy(user, giphy):
    Giphy.delete_giphy(user_id=user.id, giphy=giphy)
    return jsonify({"success": True}), 204

@bp.route("/user/<giphy>", methods=["POST"])
@token_required
def save_user_giphy(user, giphy):
    try:
        giphy = Giphy(user_id=user.id, giphy=giphy)
        db_session.add(giphy)
        db_session.commit()
        return jsonify({"success": True, "message": "Saved giphy"}), 201
    except Exception as ex:
        return jsonify({"success": False, "message": "Already in your profile"}), 405
