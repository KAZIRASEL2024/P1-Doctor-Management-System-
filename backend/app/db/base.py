"""SQLAlchemy declarative base and metadata."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """All ORM models inherit from this class."""
    pass
