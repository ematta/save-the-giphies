from flask import Blueprint, jsonify, request
from save_the_giphies.libraries.retriever import retriever

bp = Blueprint(
    "giphy",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/giphy",
)

@bp.route("/")
def index():
    search_query = request.args.get("query")
    response = retriever.retrieve_giphies(query=search_query)
    return jsonify(response)
