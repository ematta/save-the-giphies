import logging

logger: "logging.Logger" = logging.getLogger(__name__)

c_handler: "logging.StreamHandler" = logging.StreamHandler()
c_format: "logging.Formatter" = logging.Formatter(
    "%(name)s - %(levelname)s - %(message)s"
)
c_handler.setLevel(logging.WARNING)
c_handler.setFormatter(c_format)

f_handler: "logging.StreamHandler" = logging.FileHandler("save_the_giphys_py.log")
f_format: "logging.Formatter" = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
f_handler.setLevel(logging.WARNING)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)
