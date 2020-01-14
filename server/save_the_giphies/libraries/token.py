from functools import wraps
import jwt
from flask import jsonify, request
from save_the_giphies.database.models import User
from save_the_giphies.config import config


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()
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
            token = auth_headers[1]
            data = jwt.decode(token, config.config["SECRET_KEY"])
            user = User.query.filter_by(email=data["sub"]).first()
            if not user:
                return (
                    jsonify({"message": "User not found.", "authenticated": False}),
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
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
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
