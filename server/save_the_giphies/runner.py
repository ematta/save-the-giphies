from flask import Flask
from flask_cors import CORS
from save_the_giphies.routes import giphy
from save_the_giphies.routes import user
from save_the_giphies.routes import tag
from save_the_giphies.database.engine import db_session
from save_the_giphies.config import config


def create_app():
    """ Creates the flask app """
    app: "Flask" = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret_key
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(giphy.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(tag.bp)

    @app.errorhandler(404)
    def not_found(error):
        """ 404 route """
        return {"message": f"Not found: {error}"}

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """ When we shit down, kill the DB Session """
        db_session.remove()

    return app
