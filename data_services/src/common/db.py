from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime
from typing import Optional, List


class Article(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    headline: str
    url: str
    author: str
    title: str
    category: str
    source: str
    date: str
    content: str


def connect(db_uri):
    engine = create_engine(db_uri, echo=True)
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    return session
