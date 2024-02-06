from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List
from typing import Optional


def connect(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    headline: Column(String)
    url: Column(String)
    author: Column(String)
    title: Column(String)
    category: Column(String)
    source: Column(String)
    date: Column(String)
    content: Column(String)


# Connect to the database
