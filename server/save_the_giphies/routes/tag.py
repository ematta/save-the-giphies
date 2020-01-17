from flask import Blueprint, jsonify, request
from save_the_giphies.database.models import Giphy
from save_the_giphies.libraries.retriever import retriever
from save_the_giphies.libraries.token import token_required
from save_the_giphies.database.engine import db_session

bp = Blueprint("tag", __name__, url_prefix="/tags",)


@bp.route("/<giphy>/<tag>", methods=["POST"])
@token_required
def save_tag(user, giphy, tag):
    try:
        giphy = Giphy.get_user_giphy(user_id=user.id, giphy=giphy)
        new_tag = Tag.save_tag(**{"giphy_id": giphy.id, "tag": tag})
        return jsonify({"success": True, "message": "Saved tag"}), 201
    except Exception as ex:
        return jsonify({"success": False, "message": "Tag already associated"}), 405


@bp.route("/<giphy>/<tag>", methods=["DELETE"])
@token_required
def delete_giphy_tag(user, giphy, tag):
    giphy = Giphy.get_user_giphy(user_id=user.id, giphy=giphy)
    Tag.delete_tag(giphy_id=giphy.id, tag=tag)
    return jsonify({"success": True}), 204

@bp.route("/<giphy>", methods=["GET"])
@token_required
def get_user_giphies(user, giphy):
    giphy = Giphy.get_user_giphy(user_id=user.id, giphy=giphy)
    all_tags = Tag.all_tags(giphy_id=giphy.id)
    tags = [
        tag.tag for tag in all_tags
    ]
    return jsonify(tags)
