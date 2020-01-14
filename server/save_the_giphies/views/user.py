from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import jwt

from save_the_giphies.database.database import db_session
from save_the_giphies.database.models import User
from save_the_giphies.config import config

bp = Blueprint("user", __name__, url_prefix="/user",)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(**data)
    db_session.add(user)
    db_session.commit()
    return jsonify(user.to_dict()), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.authenticate(**data)
    if not user:
        return jsonify({"message": "Invalid credentials", "authenticated": False}), 401
    token_data = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(token_data, config.secret_key)
    response = {"token": token.decode("UTF-8"), "user": user.to_dict()}
    return jsonify(response)
