from sqlalchemy import create_engine
from . import manager

engine = create_engine("sqlite:///mydb.db", echo=True)
