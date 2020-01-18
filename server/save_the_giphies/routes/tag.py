from flask import Blueprint, jsonify
from save_the_giphies.database.models import Giphies, Tags
from save_the_giphies.libraries.token import token_required
from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from save_the_giphies.database.models import Users
    from flask.wrappers import Response

bp = Blueprint("tag", __name__, url_prefix="/tags",)


@bp.route("/<string:giphies_id>/<string:tag>", methods=["POST"])
@token_required
def save_tag(user: "Users", giphies_id: str, tag: str) -> "Tuple[Response, int]":
    try:
        giphy: "Giphies" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
        Tags.save_tag(**{"giphies_id": giphy.id, "tag": tag})
        return jsonify({"success": True, "message": "Saved tag"}), 201
    except Exception:
        return jsonify({"success": False, "message": "Tags already associated"}), 405


@bp.route("/<string:giphies_id>/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_giphy_tag(
    user: "Users", giphies_id: str, tag_id: int
) -> "Tuple[Response, int]":
    giphy: "Giphies" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    Tags.delete_tag(giphies_id=giphy.id, tag_id=tag_id)
    return jsonify({"success": True}), 204


@bp.route("/<string:giphies_id>", methods=["GET"])
@token_required
def get_giphy_tags(user: "Users", giphies_id: str) -> "Tuple[Response, int]":
    giphy: "Giphies" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    tags: "List[Tags]" = Tags.all_tags(giphies_id=giphy.id)
    return jsonify([tag.to_dict() for tag in tags])
