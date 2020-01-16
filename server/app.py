from save_the_giphies.runner import create_app
from save_the_giphies.config import config


if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.debug)
