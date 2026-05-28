import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#loading environment variable from .env file
load_dotenv()

db_url = os.getenv("database_url")

if not db_url:
    raise ValueError("database url is not setup in .env file")

#creating database engine that enables python to talk to postgreSQL
#intermediate between these two is -> SQLAlchemy

#prepares SQLAlchemy engine for communication
engine = create_engine(db_url)

#establishing connection
try:
    with engine.connect() as conn:
        print("connection is successfull")
except Exception as e:
    print(e)


#SessionLocal is like the creator of all sessions
#autoCommit is set to false -> changes are not saved automatically(manual)
#autoFlush is set to false -> database will not automatically sync pending changes 
#bind = engine tells which database to be used to create sessions
SessionLocal = sessionmaker(autocommit = False , autoflush=False , bind=engine)

#base tells which class is actually a database model
#acts like someone who registers all tables involved
Base = declarative_base()

def get_db():

    #starting a session . db is our actual session here
    db = SessionLocal()

    try:
        #yield hands the active sessions to routes
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()







#notes for self:
#ORM -> object relational mapper 
#it is like a translator . SQLAlchemy is ORM + basic SQL


