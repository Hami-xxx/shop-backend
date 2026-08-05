from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
TEST_DATABASE_URL = "sqlite:///./test.db"
testing_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker( autocommit=False,autoflush=False,bind=testing_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
    