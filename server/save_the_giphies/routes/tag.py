from flask import Blueprint, jsonify
from save_the_giphies.database.models import Giphies, Tags
from save_the_giphies.libraries.token import token_required
from typing import TYPE_CHECKING, Tuple, List, Dict

if TYPE_CHECKING:
    from save_the_giphies.database.models import Users
    from flask.wrappers import Response

bp = Blueprint("tag", __name__, url_prefix="/tags",)


@bp.route("/<string:giphies_id>/<string:tag>", methods=["POST"])
@token_required
def save_tag(user: "Users", giphies_id: str, tag: str) -> "Tuple[Response, int]":
    """Saves tag for given giphy
    Params:
        user (Users): User model provided by token_required
        giphies_id (str): Giphy ID provided by GIPHY
        tag (str): Tag used for giphy

    Returns Tuple[Response, int]
    """
    results: "Dict" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    giphy: "Giphies" = results["giphy"]
    result: "Dict" = Tags.save_tag(**{"giphies_id": giphy.id, "tag": tag})
    status = 201 if result["success"] else 400
    return (
        jsonify({"success": result["success"], "msg": result["msg"]}),
        status,
    )


@bp.route("/<string:giphies_id>/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_giphy_tag(
    user: "Users", giphies_id: str, tag_id: int
) -> "Tuple[Response, int]":
    """Delete tag for given giphy
    Params:
        user (Users): User model provided by token_required
        giphies_id (str): Giphy ID provided by GIPHY
        tag_id (int): Tag ID associated with Tag giphy

    Returns Tuple[Response, int]
    """
    results: "Dict" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    giphy: "Giphies" = results["giphy"]
    success: "bool" = Tags.delete_tag(giphies_id=giphy.id, tag_id=tag_id)
    status: "int" = 204 if success else 404
    return jsonify({"success": success}), status


@bp.route("/<string:giphies_id>", methods=["GET"])
@token_required
def get_giphy_tags(user: "Users", giphies_id: str) -> "Tuple[Response, int]":
    """Get tags for given giphy
    Params:
        user (Users): User model provided by token_required
        giphies_id (str): Giphy ID provided by GIPHY
        tag_id (int): Tag ID associated with Tag giphy

    Returns Tuple[Response, int]
    """
    results: "Dict" = Giphies.first_giphy(users_id=user.id, giphy=giphies_id)
    tags: "List[Tags]" = []
    if results["success"]:
        giphy: "Giphies" = results["giphy"]
        tags = [tag.to_dict() for tag in Tags.all_tags(giphies_id=giphy.id)]
    return jsonify(tags), 200
