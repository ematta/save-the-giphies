from functools import wraps
import jwt
from flask import jsonify, request
from save_the_giphies.database.models import Users
from save_the_giphies.config import config
from typing import Tuple, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from flask.wrappers import Response


def token_required(f):
    """ Token checker decorator """

    @wraps(f)
    def _verify(*args, **kwargs) -> "Tuple[Response, int]":
        """ Verifies the token """
        auth_headers: "List[str]" = request.headers.get("Authorization", "").split()
        if len(auth_headers) != 2:
            return (
                jsonify(
                    {
                        "message": "Authentication header not set correctly (or token missing).",
                        "authenticated": False,
                    }
                ),
                401,
            )
        try:
            token: "str" = auth_headers[1]
            data: "Dict" = jwt.decode(token, config.secret_key)
            user: "Users" = Users.query.filter_by(email=data["sub"]).first()
            if not user:
                return (
                    jsonify({"message": "Users not found.", "authenticated": False}),
                    401,
                )
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return (
                jsonify(
                    {
                        "message": "Expired token. Reauthentication required.",
                        "authenticated": False,
                    }
                ),
                401,
            )
        except jwt.InvalidTokenError:
            return (
                jsonify(
                    {
                        "message": "Invalid token. Registeration and / or authentication required",
                        "authenticated": False,
                    }
                ),
                401,
            )

    return _verify
