from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from save_the_giphies.libraries.logger import logger
from save_the_giphies.config import config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine
    from sqlalchemy.orm.scoping import scoped_session as ss
    from sqlalchemy.ext.declarative.api import DeclarativeMeta

db_string: "str" = (
    "postgres+psycopg2://"
    f"{config.database_user}:{config.database_password}"
    f"@{config.database_url}:{config.database_port}/{config.database_schema}"
)
engine: "Engine" = create_engine(db_string, convert_unicode=True)
db_session: "ss" = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base: "DeclarativeMeta" = declarative_base()
Base.query = db_session.query_property()  # type: ignore


def init_db():
    """ Initiallizes the database """
    import save_the_giphies.database.models  # noqa: ignore=F401

    logger.info("Initializing DB")
    Base.metadata.create_all(bind=engine)


def drop_db():
    """ Drops the database """
    import save_the_giphies.database.models  # noqa: ignore=F401

    logger.info("Dropping DB")
    Base.metadata.drop_all(bind=engine)
