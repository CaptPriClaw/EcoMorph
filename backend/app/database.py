# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create the database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
# The check_same_thread argument is only needed for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This Base will be used by all of our ORM models to inherit from.
Base = declarative_base()


# --- Dependency ---
def get_db():
    """
    A dependency that provides a database session for each request,
    and then closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()