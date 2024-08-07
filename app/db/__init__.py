# app/db/__init__.py
from app.db.base_class import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)
