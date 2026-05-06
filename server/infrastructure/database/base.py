from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def build_session_factory(database_url: str, init_db: bool) -> sessionmaker:
    engine = create_engine(database_url)
    if init_db:
        Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
