from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base


# =========================================================
# PROJECT PATHS
# =========================================================

# Project root:
# D:\SIH26047
BASE_DIR = Path(__file__).resolve().parents[2]

# Persistent application database
DATA_DIR = BASE_DIR / "db" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "patient_case.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def create_tables():
    """
    Create missing database tables without deleting
    existing data.
    """
    Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()