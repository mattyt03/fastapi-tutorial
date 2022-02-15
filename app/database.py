from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# format: 'postgresql://username:password@hostname:port/dbname'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# what does an engine do?
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# what are these parameters for?
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# this function automatically opens and closes a db session
# it gets called whenever we receive a request
def get_db():
    db = SessionLocal()
    try:
        yield db  # yield?
    finally:  # finally?
        db.close()