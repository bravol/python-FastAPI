
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

# database url
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/TodoDatabase'

# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# instance of session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a database object
Base = declarative_base()
