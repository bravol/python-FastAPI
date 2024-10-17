
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

# database url
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:CISSYbravol%4075@127.0.0.1:3306/TodoDatabase'

# create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# instance of session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a database object
Base = declarative_base()
