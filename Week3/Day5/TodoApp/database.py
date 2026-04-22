from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker #hleps to create a session for interacting with the database
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db" #This will create a location of this database

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False}) #by default, SQLAlchemy does not allow multiple threads to access the same database connection. 
#The connect_args={"check_same_thread": False} argument is used to disable this check and allow multiple threads to access the same database connection. This is necessary when using SQLite in a multi-threaded environment, such as when running a web application with multiple requests being handled concurrently.

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine) #This creates a session factory that can be used to create sessions for interacting with the database. 
#The autocommit=False argument means that changes to the database will not be automatically committed after each operation 
#The autoflush=False argument means that changes will not be automatically flushed to the database until explicitly committed. 
#The bind=engine argument specifies the database engine to use for the sessions created by this factory.

Base=declarative_base() #This creates a base class/object for our database models. We will use this base class to define our database tables and their relationships.(control)