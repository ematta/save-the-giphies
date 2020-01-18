from flask import Blueprint, jsonify
from save_the_giphies.database.models import Giphies, Tags
from save_the_giphies.libraries.token import token_required

bp = Blueprint("tag", __name__, url_prefix="/tags",)


@bp.route("/<giphies_id>/<tag>", methods=["POST"])
@token_required
def save_tag(user, giphies_id, tag):
    try:
        giphy = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
        Tags.save_tag(**{"giphies_id": giphy.id, "tag": tag})
        return jsonify({"success": True, "message": "Saved tag"}), 201
    except Exception:
        return jsonify({"success": False, "message": "Tags already associated"}), 405


@bp.route("/<giphies_id>/<tag>", methods=["DELETE"])
@token_required
def delete_giphy_tag(user, giphies_id, tag):
    giphy = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    Tags.delete_tag(giphies_id=giphy.id, tag=tag)
    return jsonify({"success": True}), 204


@bp.route("/<giphies_id>", methods=["GET"])
@token_required
def get_giphy_tags(user, giphies_id):
    giphy = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    all_tags = Tags.all_tags(giphies_id=giphy.id)
    tags = [tag.tag for tag in all_tags]
    return jsonify(tags)
