from save_the_giphies.runner import create_app
from save_the_giphies.config import config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

if __name__ == '__main__':
    """ Entry point """
    app: "Flask" = create_app()
    app.run(debug=config.debug)
