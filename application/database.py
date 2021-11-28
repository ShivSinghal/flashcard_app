from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
db = SQLAlchemy() 
