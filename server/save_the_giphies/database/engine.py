from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from save_the_giphies.config import config

db_string = (
    "postgres+psycopg2://"
    f"{config.database_user}:{config.database_password}"
    f"@{config.database_url}:{config.database_port}/{config.database_schema}"
)

engine = create_engine(db_string, convert_unicode=True)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()  # type: ignore


def init_db():
    import save_the_giphies.database.models  # noqa: ignore=F401
    Base.metadata.create_all(bind=engine)

def drop_db():
    import save_the_giphies.database.models   # noqa: ignore=F401
    Base.metadata.drop_all(bind=engine)
