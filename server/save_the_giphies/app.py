from flask import Flask
from flask_cors import CORS
from save_the_giphies.views import giphy


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(giphy.bp)

    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Not here homie!"}

    return app


app = create_app()
