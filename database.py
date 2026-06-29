from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATA_BASE_URL = "sqlite:///./database.db"
engine = create_engine(DATA_BASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
